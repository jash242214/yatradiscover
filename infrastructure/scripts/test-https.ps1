# YatraDiscover AI - HTTPS & SSL Certificate Validator
# Tests HTTPS connectivity and SSL/TLS certificate validity

param(
    [string]$Domain = "yatradiscover.com",
    [switch]$Verbose
)

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║ $($Text.PadRight(58)) ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Test-HTTPS {
    param(
        [string]$URL,
        [string]$Description
    )
    
    try {
        Write-Host "  Testing: $Description" -ForegroundColor White
        
        # Test HTTPS connectivity
        $response = Invoke-WebRequest -Uri "https://$URL" -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
        
        if ($response.StatusCode -eq 200) {
            Write-Host "    ✓ HTTPS Connection: OK (Status $($response.StatusCode))" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "    ⚠ HTTPS Connection: Status $($response.StatusCode)" -ForegroundColor Yellow
            return $true
        }
    }
    catch {
        # Try to get SSL error details
        $errorMsg = $_.Exception.Message
        if ($errorMsg -like "*certificate*" -or $errorMsg -like "*SSL*") {
            Write-Host "    ✗ SSL Certificate Error: $errorMsg" -ForegroundColor Red
        }
        else {
            Write-Host "    ✗ Connection Error: $errorMsg" -ForegroundColor Red
        }
        return $false
    }
}

function Test-SSLCertificate {
    param(
        [string]$HostName,
        [string]$Description
    )
    
    try {
        Write-Host "  Checking SSL: $Description" -ForegroundColor White
        
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect($HostName, 443)
        
        $sslStream = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false)
        $sslStream.AuthenticateAsClient($HostName)
        
        $cert = $sslStream.RemoteCertificate
        
        if ($cert) {
            $certObject = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($cert)
            
            Write-Host "    ✓ Certificate Found" -ForegroundColor Green
            Write-Host "      Subject: $($certObject.Subject)" -ForegroundColor Gray
            Write-Host "      Issuer: $($certObject.Issuer)" -ForegroundColor Gray
            Write-Host "      Valid From: $($certObject.NotBefore)" -ForegroundColor Gray
            Write-Host "      Valid Until: $($certObject.NotAfter)" -ForegroundColor Gray
            
            # Check expiration
            $daysUntilExpiry = ([datetime]$certObject.NotAfter - (Get-Date)).Days
            
            if ($daysUntilExpiry -lt 0) {
                Write-Host "      Status: ✗ EXPIRED ($(([math]::Abs($daysUntilExpiry))) days ago)" -ForegroundColor Red
                return $false
            }
            elseif ($daysUntilExpiry -lt 30) {
                Write-Host "      Status: ⚠ EXPIRING SOON ($daysUntilExpiry days)" -ForegroundColor Yellow
                return $true
            }
            else {
                Write-Host "      Status: ✓ Valid ($daysUntilExpiry days remaining)" -ForegroundColor Green
                return $true
            }
        }
        else {
            Write-Host "    ✗ No certificate found" -ForegroundColor Red
            return $false
        }
        
        $sslStream.Close()
        $tcpClient.Close()
    }
    catch {
        Write-Host "    ✗ Error checking certificate: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main validation
Write-Header "YatraDiscover AI - HTTPS & SSL Certificate Check"

Write-Host "Primary Domain: $Domain" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')" -ForegroundColor Yellow
Write-Host ""

$results = @{}

# Test primary domain
Write-Host "Testing Primary Domain:" -ForegroundColor Yellow
$results["root_https"] = Test-HTTPS "$Domain" "https://$Domain"
Write-Host ""

$results["root_ssl"] = Test-SSLCertificate "$Domain" "SSL Certificate for $Domain"
Write-Host ""

# Test www subdomain
Write-Host "Testing www Subdomain:" -ForegroundColor Yellow
$results["www_https"] = Test-HTTPS "www.$Domain" "https://www.$Domain"
Write-Host ""

$results["www_ssl"] = Test-SSLCertificate "www.$Domain" "SSL Certificate for www.$Domain"
Write-Host ""

# Test API subdomain
Write-Host "Testing API Subdomain:" -ForegroundColor Yellow
$results["api_https"] = Test-HTTPS "api.$Domain" "https://api.$Domain"
Write-Host ""

$results["api_ssl"] = Test-SSLCertificate "api.$Domain" "SSL Certificate for api.$Domain"
Write-Host ""

# Test HTTP to HTTPS redirect
Write-Host "Testing HTTP Redirect:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://$Domain" -MaximumRedirection 1 -TimeoutSec 5 -UseBasicParsing
    Write-Host "  HTTP Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  ✓ HTTP accessible" -ForegroundColor Green
}
catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    if ($statusCode -ge 301 -and $statusCode -le 308) {
        Write-Host "  ✓ HTTP to HTTPS redirect configured (Status $statusCode)" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠ Unexpected HTTP status: $statusCode" -ForegroundColor Yellow
    }
}

Write-Host ""

# Summary
$passedCount = ($results.Values | Where-Object { $_ -eq $true }).Count
$totalCount = $results.Count

Write-Header "Validation Summary"

Write-Host "Total Checks: $totalCount" -ForegroundColor White
Write-Host "Passed: $passedCount / $totalCount" -ForegroundColor Green

if ($passedCount -eq $totalCount) {
    Write-Host "Status: ✅ All HTTPS and SSL checks passed" -ForegroundColor Green
}
else {
    $failedCount = $totalCount - $passedCount
    Write-Host "Status: ⚠️  $failedCount check(s) failed" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Recommended Actions:" -ForegroundColor Yellow
    Write-Host "1. Verify origin server is running and accessible"
    Write-Host "2. Check Cloudflare proxy settings"
    Write-Host "3. Configure SSL/TLS Full (strict) in Cloudflare"
    Write-Host "4. Install origin certificate on origin server"
}

Write-Host ""
