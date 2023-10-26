use aes_gcm::{
    aead::{Aead, AeadCore, KeyInit, OsRng},
    Aes256Gcm,
    // Key, // Or `Aes128Gcm`
    // Nonce,
};
use rsa::{Pkcs1v15Encrypt, RsaPrivateKey, RsaPublicKey};
use serde::{Deserialize, Serialize};
// use serde_json::Result;
use std::io::{self, Read};
// use std::time::Instant;

use rsa::pkcs1v15::{Signature, SigningKey};
use sha2::{Sha256, Digest};
use rsa::signature::{Keypair, RandomizedSigner, SignatureEncoding, Verifier};

#[derive(Serialize, Deserialize)]
struct SignedMessage {
    original_input: String,
    input_hash: String,
    hash_signature: Vec<u8>,
}

#[derive(Serialize, Deserialize)]
struct DigitalEnvelope {
    encrypted_json: Vec<u8>,
    encrypted_aes_key: Vec<u8>,
}

fn main() {
    // Read input from the terminal
    println!("Enter a string: ");
    let mut input: String = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read input");

    // Compute SHA-256 hash
    let hash: String = sha256_hash(&input);

    let mut rng: rand::rngs::ThreadRng = rand::thread_rng();
    let bits: usize = 2048;
    let private_key: RsaPrivateKey =
        RsaPrivateKey::new(&mut rng, bits).expect("failed to generate a aes_key");
    let public_key: RsaPublicKey = RsaPublicKey::from(&private_key);

    let signing_key = SigningKey::<Sha256>::new(private_key.clone());
    let verifying_key = signing_key.verifying_key();

    let signature = signing_key.sign_with_rng(&mut rng, hash.as_bytes());

    verifying_key
        .verify(hash.as_bytes(), &signature)
        .expect("failed to verify");

    // Create a JSON object
    let data: SignedMessage = SignedMessage {
        original_input: input,
        input_hash: hash,
        hash_signature: signature.to_bytes().to_vec(),
    };

    // Serialize the JSON object to a string
    let json_data: String = serde_json::to_string(&data).expect("Failed to serialize to JSON");

    let aes_key = Aes256Gcm::generate_key(OsRng);
    let cipher = Aes256Gcm::new(&aes_key);
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng); // 96-bits; unique per message
    let encrypted_json: Vec<u8> = cipher
        .encrypt(&nonce, json_data.as_bytes())
        .expect("error on aes encryption");

    // Encrypt the AES aes_key using RSA
    let enc_aes_key: Vec<u8> = public_key
        .encrypt(&mut rng, Pkcs1v15Encrypt, &aes_key[..])
        .expect("failed to encrypt");

    // Create a JSON object for the encrypted data
    let encrypted_data: DigitalEnvelope = DigitalEnvelope {
        encrypted_json,
        encrypted_aes_key: enc_aes_key,
    };

    // Serialize the encrypted data JSON object to a string
    let encrypted_json_data: String =
        serde_json::to_string(&encrypted_data).expect("Failed to serialize to JSON");


    let myj: DigitalEnvelope = serde_json::from_str(encrypted_json_data.as_str()).unwrap();

    let dec_aes_key: Vec<u8> = private_key
        .decrypt(Pkcs1v15Encrypt, &myj.encrypted_aes_key)
        .expect("failed to decrypt");

    assert_eq!(aes_key.to_vec(), dec_aes_key);

    let dec_json_data: Vec<u8> = cipher
        .decrypt(&nonce, myj.encrypted_json.as_ref())
        .expect("error on aes decryption");

    let dec_json: SignedMessage =
        serde_json::from_str(String::from_utf8(dec_json_data).unwrap().as_str()).unwrap();

    assert_eq!(
        sha256_hash(dec_json.original_input.as_str()),
        dec_json.input_hash
    );

    verifying_key
        .verify(
            dec_json.input_hash.as_bytes(),
            &Signature::try_from(dec_json.hash_signature.as_ref()).unwrap(),
        )
        .expect("failed to verify");

    println!("data received successfully: {}", dec_json.original_input);

    println!("Press Enter to close:");
    io::stdin().read(&mut [0;1]).unwrap();
}

fn sha256_hash(data: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data);
    format!("{:x}", hasher.finalize())
}
