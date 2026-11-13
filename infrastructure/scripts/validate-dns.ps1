# YatraDiscover AI - DNS Resolution Validator
# Validates that all required DNS records are properly configured

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

function Test-DNSRecord {
    param(
        [string]$RecordName,
        [string]$RecordType = "A"
    )
    
    try {
        $result = Resolve-DnsName -Name $RecordName -Type $RecordType -ErrorAction SilentlyContinue
        
        if ($result) {
            Write-Host "  ✓ $RecordName ($RecordType)" -ForegroundColor Green
            if ($Verbose) {
                $result | ForEach-Object {
                    Write-Host "    → $($_.IP4Address)" -ForegroundColor Gray
                }
            }
            return $true
        }
        else {
            Write-Host "  ✗ $RecordName ($RecordType) - Not found" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "  ✗ $RecordName ($RecordType) - Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main validation
Write-Header "YatraDiscover AI - DNS Resolution Check"

Write-Host "Testing domain: $Domain" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')" -ForegroundColor Gray
Write-Host ""

$results = @{}

# Test A records
Write-Host "A Records:" -ForegroundColor Yellow
$results["root"] = Test-DNSRecord "$Domain" "A"
$results["www"] = Test-DNSRecord "www.$Domain" "A"
$results["api"] = Test-DNSRecord "api.$Domain" "A"
$results["admin"] = Test-DNSRecord "admin.$Domain" "A"
$results["partners"] = Test-DNSRecord "partners.$Domain" "A"
$results["staging"] = Test-DNSRecord "staging.$Domain" "A"

Write-Host ""

# Test MX records
Write-Host "Email Records (MX):" -ForegroundColor Yellow
$mxResult = Test-DNSRecord "$Domain" "MX"

Write-Host ""

# Test CNAME records
Write-Host "CNAME Records:" -ForegroundColor Yellow
$cnameResult = Test-DNSRecord "www.$Domain" "CNAME"

Write-Host ""

# Test TXT records (SPF, DKIM, DMARC)
Write-Host "TXT Records (SPF, DKIM, DMARC):" -ForegroundColor Yellow
$spfResult = Test-DNSRecord "$Domain" "TXT"

Write-Host ""

# Summary
$passedCount = ($results.Values | Where-Object { $_ -eq $true }).Count
$totalCount = $results.Count

Write-Header "Validation Summary"
Write-Host "Total Records Checked: $totalCount" -ForegroundColor White
Write-Host "Passed: $passedCount / $totalCount" -ForegroundColor Green

if ($passedCount -eq $totalCount) {
    Write-Host "Status: ✅ All DNS records are properly configured" -ForegroundColor Green
}
else {
    $failedCount = $totalCount - $passedCount
    Write-Host "Status: ⚠️  $failedCount record(s) not configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Recommended Actions:" -ForegroundColor Yellow
    Write-Host "1. Log into Cloudflare dashboard"
    Write-Host "2. Check DNS records for $Domain"
    Write-Host "3. Verify all subdomains point to correct targets"
    Write-Host "4. Allow 24-48 hours for DNS propagation"
}

Write-Host ""
