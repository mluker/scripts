$myitems =
@(
    [pscustomobject]@{rg = "azure-resource-group-here"; sub = "azure-subscription-here"; server = "azure-sql-server-name-here" },
    [pscustomobject]@{rg = "azure-resource-group-here"; sub = "azure-subscription-here"; server = "azure-sql-server-name-here" },
    [pscustomobject]@{rg = "azure-resource-group-here"; sub = "azure-subscription-here"; server = "azure-sql-server-name-here" })

$ip = $(dig -4 TXT +short o-o.myaddr.l.google.com `@ns1.google.com | sed 's/^"\(.*\)"$/\1/')
$rule_name = "rule-name-here"

foreach ($item in $myitems) {
    Write-Host `n`n`n"$($item.server)"
        az sql server firewall-rule create -g $($item.rg) -s $($item.server) -n $($rule_name) --subscription $($item.sub) --start-ip-address $ip --end-ip-address $ip
}