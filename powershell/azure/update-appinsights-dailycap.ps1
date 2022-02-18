# set the daily ingestion cap for all AI instance in every resource group

Select-AzSubscription -SubscriptionName 'foobar' | Set-AzContext
$ai = Get-AzApplicationInsights | select ResourceGroupName, Name

 $AI | foreach {
     $cap = 10
     write-host ("Setting daily cap at $cap for {0} instance " -f $_.ResourceGroupName) -NoNewline
     write-host $_.Name
     Set-AzApplicationInsightsDailyCap -ResourceGroupName $_.ResourceGroupName -Name $_.Name -DailyCapGB $cap
 }