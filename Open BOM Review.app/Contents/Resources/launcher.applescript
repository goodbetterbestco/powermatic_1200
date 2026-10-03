on run arguments
    set pythonPath to item 1 of arguments
    set helperPath to item 2 of arguments
    set projectPath to item 3 of arguments
    try
        set reviewURL to do shell script (quoted form of pythonPath & " " & quoted form of helperPath & " " & quoted form of projectPath)
        tell application "Terminal"
            if (count of windows) is 0 then
                do script "printf '%s\\n' " & quoted form of ("BOM review: " & reviewURL) & " " & quoted form of "The reviewer runs in the background. You may close this window."
            end if
        end tell
        open location reviewURL
    on error errorMessage
        display alert "Could not open BOM review" message errorMessage as critical
    end try
end run
