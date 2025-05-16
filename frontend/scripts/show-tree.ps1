param(
    [int]$Depth = 2,
    [string]$Exclude = "node_modules,dist,bin"
)

function Show-Tree($path, $indent = "") {
    $items = Get-ChildItem $path -ErrorAction SilentlyContinue | 
             Where-Object { $_.Name -notin $Exclude.Split(',') }
    
    $count = $items.Count
    $i = 0
    
    foreach ($item in $items) {
        $i++
        $isLast = ($i -eq $count)
        
        if ($isLast) {
            Write-Host "$indent└── $($item.Name)" -ForegroundColor Cyan
            $newIndent = $indent + "    "
        } else {
            Write-Host "$indent├── $($item.Name)" -ForegroundColor Cyan
            $newIndent = $indent + "│   "
        }
        
        if ($item.PSIsContainer -and ($Depth -gt 0)) {
            Show-Tree $item.FullName $newIndent ($Depth - 1)
        }
    }
}

Show-Tree -path . -Depth $Depth