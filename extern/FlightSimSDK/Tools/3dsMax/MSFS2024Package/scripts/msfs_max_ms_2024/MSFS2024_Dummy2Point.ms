rollout myRollout "Dummy2Point" width:200 height:160
(
    label myLabel "Select Dummy then click Convert" width:170 pos:[15,10]
    checkbox crossCheckbox " Cross" checked:true pos:[80, 40]
    checkbox boxCheckbox " Box" checked:true pos:[80, 60]
    spinner sizeSpinner "Size of the points " pos:[80, 90] width:80 range:[0.01, 100, 0.5] type:#float scale:0.01
    button myButton "Convert" width:100 height:30 pos:[50, 120]
    
    on myButton pressed do
    (
        -- Get the size value from the spinner
        pointSize = sizeSpinner.value
        showCross = crossCheckbox.state
        showBox = boxCheckbox.state
        
        -- Store a list of objects before conversion to compare later
        local initialObjects = objects as array
        
        -- Loop through each selected object
        for obj in selection do
        (
            -- Convert the selected dummy to a point and set its size
            obj.baseObject = point size:pointSize cross:showCross box:showBox
        )
        
        -- Store a list of objects after conversion
        local newObjects = objects as array
        
        -- Check for any objects created during the process
        for o in newObjects do
        (
            -- If the object is not in the initial list and is a Point at [0,0,0], delete it
            if (findItem initialObjects o == 0) and (classof o == Point) and (o.position == [0,0,0]) then
            (
                delete o
            )
        )
        
        -- Optional: Refresh the viewport to see changes immediately
        redrawViews()

        -- Print confirmation
        print ("Action Executed! Point size: " + pointSize as string + ", Cross: " + showCross as string + ", Box: " + showBox as string) -- Display a message after executing the action
    )
)

createDialog myRollout
