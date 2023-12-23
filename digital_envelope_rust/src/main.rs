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
use rsa::signature::{Keypair, RandomizedSigner, SignatureEncoding, Verifier};
use sha2::{Digest, Sha256};

// use std::io::Write;
// use std::net::TcpStream;

#[derive(Serialize, Deserialize)]
struct SignedMessage {
    original_input: String,
    input_hash: String,
    hash_signature: Vec<u8>,
}

#[derive(Serialize, Deserialize)]
struct DigitalEnvelope {
    encrypted_signed_message: Vec<u8>,
    encrypted_aes_key: Vec<u8>,
}

fn main() {
    //sender side
    println!("Enter a string: ");
    let mut input: String = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read input");

    let hash: String = sha256_hash(&input);

    let mut rng: rand::rngs::ThreadRng = rand::thread_rng();
    let bits: usize = 2048;
    let private_key: RsaPrivateKey =
        RsaPrivateKey::new(&mut rng, bits).expect("failed to generate a original_aes_key");

    let public_key: RsaPublicKey = RsaPublicKey::from(&private_key);

    let signing_key = SigningKey::<Sha256>::new(private_key.clone());
    let verifying_key = signing_key.verifying_key();

    let signature = signing_key.sign_with_rng(&mut rng, hash.as_bytes());

    let data: SignedMessage = SignedMessage {
        original_input: input,
        input_hash: hash,
        hash_signature: signature.to_bytes().to_vec(),
    };

    let json_data: String = serde_json::to_string(&data).expect("Failed to serialize");

    let original_aes_key = Aes256Gcm::generate_key(OsRng);
    let aes_cipher = Aes256Gcm::new(&original_aes_key);
    let aes_nonce = Aes256Gcm::generate_nonce(&mut OsRng); // 96-bits; unique per message
    let encrypted_signed_message: Vec<u8> = aes_cipher
        .encrypt(&aes_nonce, json_data.as_bytes())
        .expect("error on aes encryption");

    let encrypted_aes_key: Vec<u8> = public_key
        .encrypt(&mut rng, Pkcs1v15Encrypt, &original_aes_key[..])
        .expect("failed to encrypt");

    let envelope: DigitalEnvelope = DigitalEnvelope {
        encrypted_signed_message,
        encrypted_aes_key: encrypted_aes_key,
    };

    let encrypted_json_data: String =
        serde_json::to_string(&envelope).expect("Failed to serialize");

        
    //receiver side

    let received_envelope: DigitalEnvelope =
        serde_json::from_str(encrypted_json_data.as_str()).expect("failed to deserialize");

    let decrypted_aes_key: Vec<u8> = private_key
        .decrypt(Pkcs1v15Encrypt, &received_envelope.encrypted_aes_key)
        .expect("failed to decrypt AES key using RSA");

    assert_eq!(original_aes_key.to_vec(), decrypted_aes_key);

    let decrypted_json_string: Vec<u8> = aes_cipher
        .decrypt(
            &aes_nonce,
            received_envelope.encrypted_signed_message.as_ref(),
        )
        .expect("failed to decrypt signed message using AES");

    let decrypted_signed_message: SignedMessage = serde_json::from_str(
        String::from_utf8(decrypted_json_string)
            .expect("failed to convert received signed message to string")
            .as_str(),
    )
    .expect("failed to deserialize");

    assert_eq!(
        sha256_hash(decrypted_signed_message.original_input.as_str()),
        decrypted_signed_message.input_hash
    );

    verifying_key
        .verify(
            decrypted_signed_message.input_hash.as_bytes(),
            &Signature::try_from(decrypted_signed_message.hash_signature.as_ref())
                .expect("failed to export signature text to actual signature type"),
        )
        .expect("failed to verify signature");

    println!(
        "data received successfully: {}",
        decrypted_signed_message.original_input
    );

    println!("Press Enter to close:");
    io::stdin().read(&mut [0; 1]).unwrap();
}

fn sha256_hash(data: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data);
    format!("{:x}", hasher.finalize())
}
