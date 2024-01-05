from zapv2 import ZAPv2

# refrence https://medium.com/womenintechnology/owasp-zap-apisini-kullanarak-python-ile-g%C3%BCvenlik-testi-e5ac718ed66b

target_url = 'https://digikala.com'

# ZAP proxy should be running at http://localhost:8090 by default
zap = ZAPv2(proxies={'http': 'http://localhost:8090', 'https': 'http://localhost:8090'})

# Spider the target to find all accessible URLs
print('Spidering target %s' % target_url)
zap.spider.scan(target_url)
zap.spider.wait_for_completion()

# Perform active scanning for vulnerabilities
print('Scanning target %s' % target_url)
zap.ascan.scan(target_url)
zap.ascan.wait_for_completion()

# Get a summary of the alerts found during the scan
alerts = zap.core.alerts()
if alerts:
    print('\nAlerts:')
    for alert in alerts:
        print(f"Alert: {alert['alert']} at URL: {alert['url']}")

# Save the session and generate a report
session_name = 'example_session'
print(f'Saving session: {session_name}')
zap.core.save_session(session_name, overwrite=True)

# Generate HTML and XML reports
print('Generating reports')
zap.core.htmlreport()
zap.core.xmlreport()

print('Done!')
