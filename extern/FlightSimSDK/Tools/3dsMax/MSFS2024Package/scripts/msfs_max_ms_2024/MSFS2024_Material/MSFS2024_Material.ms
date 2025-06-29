if not NitrousGraphicsManager.IsEnabled() then
	messageBox "Microsoft Flight Simulator 2024 Material works in Direct3D 11 mode only, please switch viewport display driver.\n*Customize/Preferences/Viewports/Choose Driver...*" title:"Flight Simulator" beep:true

rcmenu MSFS2024MaterialRCMenuTex
(
	menuItem rc_display "Display" enabled:false
	menuItem rc_open "Open" enabled:false
	menuItem rc_explore "Explore" enabled:false
	separator sep1
	subMenu "Flags"
	(
		-- Flags Asobo
		menuItem rc_tQualityHigh "Quality High" enabled:false checked:false

		-- Flags MSFS
		menuItem rc_tAlphaPreservation "Alpha Preservation" enabled:false checked:false
		menuItem rc_tNoReduce "No Reduction" enabled:false checked:false

		-- Flags Asobo
		menuItem rc_tNoMipmaps "No Mipmaps" enabled:false checked:false
		menuItem rc_tPreComputedInvAvg "PreComputed InvAvg" enabled:false checked:false

		subMenu "Anisotropic" 
		(
			menuItem rc_tAnisotropic0x "0x (Standard)" enabled:false checked:false
			menuItem rc_tAnisotropic2x "2x (High)" enabled:false checked:false
			menuItem rc_tAnisotropic4x "4x (Very High)" enabled:false checked:false
			menuItem rc_tAnisotropic8x "8x (Extreme)" enabled:false checked:false
			menuItem rc_tAnisotropic16x "16x (Insane)" enabled:false checked:false
		)

		separator sep2
		menuItem rc_tEdit "Edit Flags File" enabled:false
		menuItem rc_tDelete "Delete Flags File" enabled:false
	)
	separator sep3
	menuItem rc_copy "Copy" enabled:false
	menuItem rc_paste "Paste" enabled:false
	menuItem rc_reload "Reload" enabled:false
	menuItem rc_remove "Remove" enabled:false
	
	local mtl
	local clipboardClass
	local basename
	local filename
	local TFlagsFile
	
	fn updateTooltipFlags =
	(
		mtl.texturesUI.updateUiFlags basename
	)
	
	fn createTFlagsFile =
	(
		if doesFileExist TFlagsFile then
		(
			return true
		)
		else
		(
			local newFile = createFile TFlagsFile
			if newFile == undefined do return false
			close newFile
			return true
		)
	)
	
	fn getFlag flagStr =
	(
		local file = openFile TFlagsFile mode:"rtS"
		local content = readDelimitedString file #eof
		close file
		
		local pos = (findString content flagStr)
		if pos != undefined then
			return true
		else
			return false
	)
	
	fn setFlag flagStr =
	(
		local file = openFile TFlagsFile mode:"rtS"
		local content = readDelimitedString file #eof
		close file
		
		if (findString content "_DEFAULT=") == undefined then content = "_DEFAULT="
		
		local pos = (findString content flagStr)
		if pos != undefined then
		(
			content = substituteString content ("+"+flagStr) ""
			content = substituteString content flagStr ""
		)
		else
			append content ("+"+flagStr)
			
		file = openFile TFlagsFile mode:"wtSc"
		format content to:file
		flush file
		close file
		updateTooltipFlags()
	)

	fn getAniso =
	(
		local file = openFile TFlagsFile mode:"rtS"
		local content = readDelimitedString file #eof
		close file
		
		local pos = (findString content "ANISOTROPIC=")
		if pos != undefined then
		(
			local n = (substring content (pos+12) 1) as integer
			if n == 1 then
				n = (substring content (pos+12) 2) as integer
			
			return n
		)
		else
			return undefined
	)
	
	fn setAniso n =
	(
		-- mtl.setAniso n basenamemax
		
		local file = openFile TFlagsFile mode:"rtS"
		local content = readDelimitedString file #eof
		close file
		
		if (findString content "_DEFAULT=") == undefined then content = "_DEFAULT="
		
		local pos = (findString content "ANISOTROPIC=")
		if pos != undefined then
		(
			local oldn = (substring content (pos+12) 1) as integer
			if oldn == 1 then
				content = replace content (pos+12) 2 (n as string)
			else
				content = replace content (pos+12) 1 (n as string)
		)
		else
			append content ("+ANISOTROPIC="+n as string)
		
		file = openFile TFlagsFile mode:"wtSc"
		format content to:file
		flush file
		close file
		updateTooltipFlags()
	)
	
	fn unsetAniso =
	(
		-- mtl.setAniso 0 basename
		
		if doesFileExist TFlagsFile then
		(
			local file = openFile TFlagsFile mode:"rtS"
			local content = readDelimitedString file #eof
			close file
			
			n=16
			while n>1 do
			(
				content = substituteString content ("+ANISOTROPIC=" + n as string) ""
				content = substituteString content ("ANISOTROPIC=" + n as string) ""
				n /= 2
			)
			
			file = openFile TFlagsFile mode:"wtSc"
			format content to:file
			flush file
			close file
			updateTooltipFlags()
		)
	)
	
	fn deleteTFlags =
	(
		if doesFileExist TFlagsFile then
		(
			if queryBox ("Suprimer le fichier .TFlags ?\n"+TFlagsFile) title:"TFlags" beep:false then
			(
				deleteFile TFlagsFile
			)
		)
		else print "Fichier TFlags inexistant"
		updateTooltipFlags()
	)
	
	on MSFS2024MaterialRCMenuTex open do
	(
		mtl = undefined
		if MatEditor.mode == #basic then --TODO get slate editor mtl, only possible in 3ds >= 2017 SP3
			mtl = medit.GetCurMtl()
		else if MatEditor.mode == #advanced then
			mtl = sme.GetMtlInParamEditor()
		
		if mtl != undefined then
		(
			clipboardClass = dotNetClass "System.Windows.Forms.Clipboard" --create a Clipboard dotNetClass
			basename = mtl.texturesUI.activeTex
			filename = mapPaths.getFullFilePath (getProperty mtl (basename + "Tex"))
			
			if filename != "" then
			(
				rc_reload.enabled = rc_explore.enabled = rc_remove.enabled = true
				if doesFileExist filename then
				(
					rc_copy.enabled = rc_display.enabled = rc_open.enabled = true
					
					rc_tAlphaPreservation.enabled = true
					rc_tNoReduce.enabled = true
					rc_tQualityHigh.enabled = true
					rc_tNoMipmaps.enabled = true
					rc_tAnisotropic0x.enabled = \
					rc_tAnisotropic2x.enabled = \
					rc_tAnisotropic4x.enabled = \
					rc_tAnisotropic8x.enabled = \
					rc_tAnisotropic16x.enabled = \
					rc_tPreComputedInvAvg.enabled = \

					rc_tEdit.enabled = true
					
					TFlagsFile = filename + ".FLAGS"
					if doesFileExist TFlagsFile then
					(
						rc_tDelete.enabled = true
						
						rc_tAlphaPreservation.checked = getFlag "ALPHAPRESERVATION"
						rc_tNoReduce.checked = getFlag "NOREDUCE"
						rc_tQualityHigh.checked = getFlag "QUALITYHIGH"
						rc_tNoMipmaps.checked = getFlag "NOMIPMAP"
						rc_tPreComputedInvAvg.checked = getFlag "PRECOMPUTEDINVAVG"

						local n = getAniso()
						case n of
						(
							-- 2: rc_tAnisotropic2x.checked = getFlag "ANISOTROPIC=2"
							-- 4: rc_tAnisotropic4x.checked = getFlag "ANISOTROPIC=4"
							-- 8: rc_tAnisotropic8x.checked = getFlag "ANISOTROPIC=8"
							-- 16: rc_tAnisotropic16x.checked = getFlag "ANISOTROPIC=16"
							-- default: rc_tAnisotropic0x.checked = getFlag "ANISOTROPIC=0"
							2: rc_tAnisotropic2x.checked = true
							4: rc_tAnisotropic4x.checked = true
							8: rc_tAnisotropic8x.checked = true
							16: rc_tAnisotropic16x.checked = true
							default: rc_tAnisotropic0x.checked = true
						)
					)else rc_tAnisotropic0x.checked = true
				)
			)
			else if getProperty mtl (basename + "Tex") != "" then --tex not found
			(
				filename = getProperty mtl (basename + "Tex")
				rc_reload.enabled = rc_explore.enabled = rc_remove.enabled = true
			)
			
			if clipboardClass.ContainsText() then
			(
				rc_paste.enabled = case tolower (getFilenameType (clipboardClass.GetText())) of
				(
					(".tif"): true
					(".dds"): true
					(".jpg"): true
					(".tga"): true 
					(".png"): true
					(".bmp"): true
					(".hdr"): true
					default: false
				)
			)
		)
	)

	on rc_display picked do
	(
		display ( openBitMap filename )
	)
	on rc_open picked do
	(
		HiddenDOSCommand filename donotwait:true
	)
	on rc_explore picked do
	(
		HiddenDOSCommand ("start \"\" \"explorer.exe\" /select," + filename)
	)
	
	on rc_tAlphaPreservation picked do if createTFlagsFile() then setFlag "ALPHAPRESERVATION"
	on rc_tNoReduce picked do if createTFlagsFile() then setFlag "NOREDUCE"
	on rc_tQualityHigh picked do if createTFlagsFile() then setFlag "QUALITYHIGH"
	on rc_tNoMipmaps picked do if createTFlagsFile() then setFlag "NOMIPMAP"
	on rc_tPreComputedInvAvg picked do if createTFlagsFile() then setFlag "PRECOMPUTEDINVAVG"

	on rc_tAnisotropic0x picked do unsetAniso()
	on rc_tAnisotropic2x picked do if createTFlagsFile() then setAniso 2
	on rc_tAnisotropic4x picked do if createTFlagsFile() then setAniso 4
	on rc_tAnisotropic8x picked do if createTFlagsFile() then setAniso 8
	on rc_tAnisotropic16x picked do if createTFlagsFile() then setAniso 16

	on rc_tEdit picked do if createTFlagsFile() then shellLaunch TFlagsFile ""
	on rc_tDelete picked do deleteTFlags()
	
	on rc_copy picked do
	(
		clipboardClass.SetText filename
	)
	on rc_paste picked do
	(
		mtl.texturesUI.loadTex (clipboardClass.GetText()) basename
	)
	on rc_reload picked do
	(
		mtl.texturesUI.loadTex filename basename
	)
	on rc_remove picked do
	(
		mtl.texturesUI.clearTex basename
	)
)

fn MSFS2024_getUiScale =
(
	local desktopSize = sysInfo.desktopSize
	local unscaledDesktopSize = sysInfo.DesktopSizeUnscaled
	local uiScale = 1.0
	-- didnt find anything in mxs help.. again. thank you autodesk
	if (abs unscaledDesktopSize.x > abs unscaledDesktopSize.y) then
	(
		if (unscaledDesktopSize.x != 0) then uiScale = unscaledDesktopSize.x as float / desktopSize.x as float
		else if (unscaledDesktopSize.y != 0) then uiScale = unscaledDesktopSize.y as float / desktopSize.y as float
	)
	else
	(
		if (unscaledDesktopSize.y != 0) then uiScale = unscaledDesktopSize.y as float / desktopSize.y as float
		else if (unscaledDesktopSize.x != 0) then uiScale = unscaledDesktopSize.x as float / desktopSize.x as float
	)
	uiScale
)

/* DISABLED custom bitmap preview by default */
/* TODO: should put this in external file and set functions as globals */
global MSFS2024_activeFramelessTexturePreview
global MSFS2024_framelessTexturePreview
global MSFS2024_framelessTextureInfos
global MSFS2024_framelessTexturePreviewBG
-- following 3 are to "fix" texture preview flickering because of bad DPI handling. Did not find any solution if preview it outside of screen for now
global MSFS2024_framelessTexturePreviewScreenOffsets
global MSFS2024_framelessTexturePreviewLastMousePos
global MSFS2024_framelessTexturePreviewLastCreateTime
fn MSFS2024_isTexturePreviewActive =
(
	if MSFS2024_activeFramelessTexturePreview == undefined then MSFS2024_activeFramelessTexturePreview = false
	MSFS2024_activeFramelessTexturePreview
)
fn MSFS2024_setTexturePreviewActive state =
(
	MSFS2024_activeFramelessTexturePreview = state
)
fn MSFS2024_hideTexturePreview =
(
	if MSFS2024_isTexturePreviewActive() then
	(
		try
		(
			DestroyDialog MSFS2024_framelessTexturePreview
			DestroyDialog MSFS2024_framelessTextureInfos
		)
		catch ()
	)
)
fn MSFS2024_displayTexturePreview slot basename =
(
	if MSFS2024_isTexturePreviewActive() then
	(
		MSFS2024_hideTexturePreview()
		sleep 0.3
		
		-- Get texture filePath
		local texturePath
		if (basename != undefined) then
		(
			local mtl
			if MatEditor.mode == #basic then --TODO get slate editor mtl, only possible in 3ds >= 2017 SP3
				mtl = medit.GetCurMtl()
			else if MatEditor.mode == #advanced then
				mtl = sme.GetMtlInParamEditor()
			
			if mtl != undefined then
			(
				local filename = mapPaths.getFullFilePath (getProperty mtl (basename + "Tex"))
				if filename != "" then texturePath = filename
			)
		)
		
		if texturePath != undefined then
		(
			if (FileResolutionManager.getFullFilePath texturePath #Bitmap) then
			(
				local bmpTex = openBitMap texturePath
				if bmpTex != undefined then
				(
					-- get current screen size and relevant positions
					local createTime = timeStamp() / 1000 -- in seconds
					local createPos = mouse.screenpos
					local unscaledCreatePos = mouse.screenposUnscaled
					local uiScale = MSFS2024_getUiScale()
					local dnPos = dotNetObject "System.Drawing.Point" unscaledCreatePos.x unscaledCreatePos.y
					local screen = (dotNetClass "System.Windows.Forms.Screen").GetBounds dnPos
					local screenSize = [screen.width, screen.height]
					local screenOffset = [screen.x, screen.y]
					local inScreenPos = unscaledCreatePos - screenOffset
					
					local screens = (dotNetClass "System.Windows.Forms.Screen").AllScreens
					
					-- init screen offsets
					if MSFS2024_framelessTexturePreviewScreenOffsets == undefined then
					(
						MSFS2024_framelessTexturePreviewScreenOffsets = for i = 1 to screens.count collect [20,20]
					)
					
					local currentScreenId = 0
					for s = 1 to screens.count while currentScreenId == 0 do
					(
						local sb = screens[s].Bounds
						local sSize = [sb.width, sb.height]
						local sOffset = [sb.x, sb.y]
						if (sSize == screenSize and sOffset == screenOffset) then
						(
							currentScreenId = s
						)
					)
					
	-- 				--local scn = slot.DeviceDpi
	-- 				--local dpi = (dotNetClass "System.Windows.Forms.Application")
	-- 				
	-- 				format "createPos: %\n" createPos
	-- 				format "unscaledCreatePos: %\n" unscaledCreatePos
	-- 				format "desktopSize: %\n" sysInfo.desktopSize
	-- 				format "unscaledDesktopSize: %\n" sysInfo.DesktopSizeUnscaled
	-- 				format "uiScale: %\n" uiScale
	-- 				--format "DeviceDpi: %\n" scn
	-- 				--format "dpi: %\n" dpi
	-- 				format "screens: %\n" scns
	-- 				format "currentScreenId: %\n" currentScreenId
	-- 				format "screenSize/screenOffset: % %\n" screenSize screenOffset
	-- 				format "inScreenPos: %\n" inScreenPos
	-- 				format "\n"
					
					-- TODO: avoid parsing file each time preview is opened...
					-- TFlags
					local TFlagsFile = getFilenamePath texturePath + (filenameFromPath texturePath) + ".FLAGS"
					local TFlags = ""
					local stream = openFile TFlagsFile
					if stream != undefined then
					(
						TFlags = "TFlags:\n"
						TFlags += readDelimitedString stream #eof
						close stream
					)
					
					-- Tooltip
					local slotName = slot.text
					local texName = filenameFromPath texturePath
					local texInfos = ""
					local texFlags = ""
	-- 				local texPath = getFilenamePath texturePath
					
					local bminfo = getBitmapInfo bmpTex
					texInfos = bminfo[3] as string + "x"+ bminfo[4] as string + "px," \
								+ " alpha channel: " + (if bminfo[9] then "YES," else "NO,") \
								+ " " + bminfo[5] as string + " bits per pixel"
					texFlags = "Flags: " + (if TFlags != "" then TFlags else "none")
					
					local minWidth = 512 / uiScale
					local texSize = [bmpTex.width, bmpTex.height]
					local safeMarginTexSize = (texSize + 40) * uiScale -- 20px margin each side - used to rescale preview if too large
					local previewSize = texSize / uiScale
					local bmpStyle = #bmp_center
					local previewScaling = 1.0
					if screenSize.x < safeMarginTexSize.x or screenSize.y < safeMarginTexSize.y then
					(
						bmpStyle = #bmp_stretch
						local scaleX = screenSize.x as float / safeMarginTexSize.x as float
						local scaleY = screenSize.y as float / safeMarginTexSize.y as float
						previewScaling = amin scaleX scaleY
						previewSize *= previewScaling
					)
					local texPreviewSizeX = previewSize.x
					previewSize.x = amax previewSize.x minWidth
					
					local textPreviewScale = "Display scale: "+((previewScaling * 100.0) as integer) as string+"%"
					
					local infoTopMargin = 4
					local infoLineHeight = 20
					local infoLinesNb = 4
					local infoSize = [previewSize.x, infoTopMargin+infoLineHeight*infoLinesNb]
					
					local taskBarSafeMargin = 40
					
					-- offset position depending on the screen. If preview flickers, we might have a wrong offset due to poor DPI handling from max: lets try to offset.
					-- no solution if preview is actually outside of screen tho :(
					if MSFS2024_framelessTexturePreviewLastMousePos == createPos then
					(
						if MSFS2024_framelessTexturePreviewLastCreateTime < createTime + 1 then
						(
							MSFS2024_framelessTexturePreviewScreenOffsets[currentScreenId].x += 50
						)
					)
					
					MSFS2024_framelessTexturePreviewLastCreateTime = createTime
					MSFS2024_framelessTexturePreviewLastMousePos = createPos
					
					local createOffset = MSFS2024_framelessTexturePreviewScreenOffsets[currentScreenId]
					
					local placeTop = -createOffset.y - previewSize.y
					local placeBottom = createOffset.y
					local placeLeft = -createOffset.x - previewSize.x
					local placeRight = createOffset.x
					
					-- by default, place bottom right
					local placeX = placeRight
					local placeY = placeBottom
					if (screenSize.x - inScreenPos.x - (createOffset.x * uiScale) < previewSize.x * uiScale) then placeX = placeLeft
					if (screenSize.y - inScreenPos.y - ((taskBarSafeMargin + createOffset.y) * uiScale) < previewSize.y * uiScale) then placeY = placeTop
					local bmpCreatePos = createPos + [placeX, placeY]
					if (bmpCreatePos.y - infoSize.y) < 0 then bmpCreatePos.y = infoSize.y -- clamp pos inside screen
					local infoCreatePos = bmpCreatePos + [0, -infoSize.y]
					
					-- create BG to reuse each time we display a preview
					if MSFS2024_framelessTexturePreviewBG == undefined then
					(
						-- checker texture
	-- 					local texBg = bitmap 16 16 color:(color 255 255 255)
	-- 					for x = 0 to texBg.width - 1 do
	-- 					(
	-- 						local halfX = 2 * x / texBg.width -- working with ints here
	-- 						for y = 0 to texBg.height - 1 do
	-- 						(
	-- 							local halfY = 2 * y / texBg.height -- working with ints here
	-- 							local checkerTex = abs (halfY - halfX)
	-- 							local checkerVal = checkerTex * 128 + 127
	-- 							local col = color checkerVal checkerVal checkerVal
	-- 							setPixels texBg [x, y] #(col)
	-- 						)
	-- 					)
						-- black texture
						local texBg = bitmap 1 1 color:(color 0 0 0)
						MSFS2024_framelessTexturePreviewBG = texBg
					)
					
					local lbFontBold = dotNetObject "System.Drawing.Font" "Arial" 16 (dotNetClass "System.Drawing.FontStyle").bold (dotNetClass "System.Drawing.GraphicsUnit").Pixel
					local lbFontItalic = dotNetObject "System.Drawing.Font" "Arial" 14 (dotNetClass "System.Drawing.FontStyle").italic (dotNetClass "System.Drawing.GraphicsUnit").Pixel
					local lbFont = dotNetObject "System.Drawing.Font" "Arial" 16 (dotNetClass "System.Drawing.GraphicsUnit").Pixel
					local lbBorderStyle = (dotNetClass "System.Windows.Forms.BorderStyle").None --FixedSingle
					local lbBgColor = (dotnetclass "system.drawing.color").FromArgb 249 249 249
					local lbFgColor = (dotnetclass "system.drawing.color").FromArgb 87 87 87
					local lbMargin = dotNetObject "System.Windows.Forms.Padding" 0 0 0 0
					local lbPadding = dotNetObject "System.Windows.Forms.Padding" 0 0 0 0
					local lbTextAlign = (dotNetClass "System.Windows.Forms.HorizontalAlignment").Center
					local lbTextAlignRight = (dotNetClass "System.Windows.Forms.HorizontalAlignment").Right
					
					rollout MSFS2024_framelessTexturePreview "Texture preview"
					(
						imgTag texBg "" pos:[0,0] opacity:1.0 transparent:(color 255 255 255) -- used as black background for now
						imgTag tex "" pos:[0,0] opacity:1.0 transparent:(color 0 0 0)
						dotNetControl dncDisplayScale	"System.Windows.Forms.Textbox" width:100 height:14
					)
					
					local inOffset = (previewSize.x - texPreviewSizeX) / 2.0
					createDialog MSFS2024_framelessTexturePreview pos:bmpCreatePos width:previewSize.x height:previewSize.y style:#() --bitmap:texBg bmpstyle:#bmp_tile
					MSFS2024_framelessTexturePreview.texBg.bitmap = MSFS2024_framelessTexturePreviewBG
	-- 				MSFS2024_framelessTexturePreview.texBg.style = #bmp_tile
					MSFS2024_framelessTexturePreview.texBg.style = #bmp_stretch
					MSFS2024_framelessTexturePreview.texBg.width = texPreviewSizeX
					MSFS2024_framelessTexturePreview.texBg.height = previewSize.y
					MSFS2024_framelessTexturePreview.texBg.pos.x = inOffset
					MSFS2024_framelessTexturePreview.tex.bitmap = bmpTex
					MSFS2024_framelessTexturePreview.tex.style = bmpStyle
					MSFS2024_framelessTexturePreview.tex.width = texPreviewSizeX
					MSFS2024_framelessTexturePreview.tex.height = previewSize.y
					MSFS2024_framelessTexturePreview.tex.pos.x = inOffset
					MSFS2024_framelessTexturePreview.dncDisplayScale.width = 100
					MSFS2024_framelessTexturePreview.dncDisplayScale.height = 14
					MSFS2024_framelessTexturePreview.dncDisplayScale.pos = [previewSize.x-inOffset-100,0]
					MSFS2024_framelessTexturePreview.dncDisplayScale.Margin = lbMargin
					MSFS2024_framelessTexturePreview.dncDisplayScale.Padding = lbPadding
					MSFS2024_framelessTexturePreview.dncDisplayScale.TextAlign = lbTextAlign
					MSFS2024_framelessTexturePreview.dncDisplayScale.text = textPreviewScale
					MSFS2024_framelessTexturePreview.dncDisplayScale.Font = lbFontItalic
					MSFS2024_framelessTexturePreview.dncDisplayScale.BorderStyle = lbBorderStyle
					MSFS2024_framelessTexturePreview.dncDisplayScale.BackColor = lbBgColor
					MSFS2024_framelessTexturePreview.dncDisplayScale.ForeColor = lbFgColor
					MSFS2024_framelessTexturePreview.dncDisplayScale.visible = previewScaling != 1.0
					
					
					rollout MSFS2024_framelessTextureInfos "Texture infos"
					(
						dotNetControl dncSlotName		"System.Windows.Forms.Textbox" width:500 height:20 align:#left
						dotNetControl dncTexName		"System.Windows.Forms.Textbox" width:500 height:20 align:#left
						dotNetControl dncInfos			"System.Windows.Forms.Textbox" width:500 height:20 align:#left
						dotNetControl dncFlags			"System.Windows.Forms.Textbox" width:500 height:20 align:#left
	-- 					dotNetControl dncTexPath		"System.Windows.Forms.Textbox" width:500 height:20 align:#left
					)
					createDialog MSFS2024_framelessTextureInfos pos:infoCreatePos width:infoSize.x height:infoSize.y style:#() bgcolor:(color 249 249 249) fgcolor:(color 87 87 87)
					MSFS2024_framelessTextureInfos.dncSlotName.width = infoSize.x-- * uiScale
					MSFS2024_framelessTextureInfos.dncSlotName.pos = [0,infoTopMargin+infoLineHeight*0]
					MSFS2024_framelessTextureInfos.dncSlotName.Margin = lbMargin
					MSFS2024_framelessTextureInfos.dncSlotName.Padding = lbPadding
					MSFS2024_framelessTextureInfos.dncSlotName.TextAlign = lbTextAlign
					MSFS2024_framelessTextureInfos.dncSlotName.text = slotName
					MSFS2024_framelessTextureInfos.dncSlotName.Font = lbFont
					MSFS2024_framelessTextureInfos.dncSlotName.BorderStyle = lbBorderStyle
					MSFS2024_framelessTextureInfos.dncSlotName.BackColor = lbBgColor
					MSFS2024_framelessTextureInfos.dncSlotName.ForeColor = lbFgColor
					MSFS2024_framelessTextureInfos.dncTexName.width = infoSize.x-- * uiScale
					MSFS2024_framelessTextureInfos.dncTexName.pos = [0,infoTopMargin+infoLineHeight*1]
					MSFS2024_framelessTextureInfos.dncTexName.Margin = lbMargin
					MSFS2024_framelessTextureInfos.dncTexName.Padding = lbPadding
					MSFS2024_framelessTextureInfos.dncTexName.TextAlign = lbTextAlign
					MSFS2024_framelessTextureInfos.dncTexName.text = texName
					MSFS2024_framelessTextureInfos.dncTexName.Font = lbFontBold
					MSFS2024_framelessTextureInfos.dncTexName.BorderStyle = lbBorderStyle
					MSFS2024_framelessTextureInfos.dncTexName.BackColor = lbBgColor
					MSFS2024_framelessTextureInfos.dncTexName.ForeColor = lbFgColor
					MSFS2024_framelessTextureInfos.dncInfos.width = infoSize.x-- * uiScale
					MSFS2024_framelessTextureInfos.dncInfos.pos = [0,infoTopMargin+infoLineHeight*2]
					MSFS2024_framelessTextureInfos.dncInfos.Margin = lbMargin
					MSFS2024_framelessTextureInfos.dncInfos.Padding = lbPadding
					MSFS2024_framelessTextureInfos.dncInfos.TextAlign = lbTextAlign
					MSFS2024_framelessTextureInfos.dncInfos.text = texInfos
					MSFS2024_framelessTextureInfos.dncInfos.Font = lbFont
					MSFS2024_framelessTextureInfos.dncInfos.BorderStyle = lbBorderStyle
					MSFS2024_framelessTextureInfos.dncInfos.BackColor = lbBgColor
					MSFS2024_framelessTextureInfos.dncInfos.ForeColor = lbFgColor
					MSFS2024_framelessTextureInfos.dncFlags.width = infoSize.x-- * uiScale
					MSFS2024_framelessTextureInfos.dncFlags.pos = [0,infoTopMargin+infoLineHeight*3]
					MSFS2024_framelessTextureInfos.dncFlags.Margin = lbMargin
					MSFS2024_framelessTextureInfos.dncFlags.Padding = lbPadding
					MSFS2024_framelessTextureInfos.dncFlags.TextAlign = lbTextAlign
					MSFS2024_framelessTextureInfos.dncFlags.text = texFlags
					MSFS2024_framelessTextureInfos.dncFlags.Font = lbFont
					MSFS2024_framelessTextureInfos.dncFlags.BorderStyle = lbBorderStyle
					MSFS2024_framelessTextureInfos.dncFlags.BackColor = lbBgColor
					MSFS2024_framelessTextureInfos.dncFlags.ForeColor = lbFgColor
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.width = infoSize.x-- * uiScale
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.pos = [0,infoTopMargin+infoLineHeight*4]
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.Margin = lbMargin
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.Padding = lbPadding
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.TextAlign = lbTextAlign
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.text = texPath
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.Font = lbFontItalic
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.BorderStyle = lbBorderStyle
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.BackColor = lbBgColor
	-- 				MSFS2024_framelessTextureInfos.dncTexPath.ForeColor = lbFgColor
				)
			)
		)
	)
)


global MSFS2024_paramsRolledUp = true
global MSFS2024_texturesRolledUp = true

plugin material MSFS2024_Material
name:"Microsoft Flight Simulator 2024"
classID:#(0x627be308, 0x1c79568e)
extends:DirectX_9_Shader replaceUI:true autoPromoteDelegateProps:false
version:2
(
	local TexList = #(
		"BaseColor",
		"OcclusionRoughnessMetallic",
		"Normal",
		"BlendMask",
		"FoliageMask",
		"Emissive",
		"WetnessAO",
		"Opacity",
		"Dirt",
		"DirtOcclusionRoughnessMetallic",
		"DetailColor",
		"DetailOcclusionRoughnessMetallic",
		"DetailNormal",
		"Occlusion",
		"ClearcoatColorRoughness",
		"ClearcoatNormal",
		"AnisoDirectionRoughness",
		"WindshieldDetailNormal",
		"ScratchesNormal",
		"WiperMask",
		"IridescentThickness",
		"WindshieldInsects",
		"WindshieldInsectsMask",
		"TireDetails",
		"TireMudNormal"
		-- Porthole parallax Interior
		/*"PHPIInteriorHallwayAlbedo",
		"PHPIInteriorHallwayNormalAo",
		"PHPIInteriorHallwayEmissive",
		"PHPIInteriorLeftWallAlbedo",
		"PHPIInteriorLeftWallNormalAo",	
		"PHPIInteriorLeftWallEmissive",	
		"PHPIInteriorRightWallAlbedo",
		"PHPIInteriorRightWallNormalAo",
		"PHPIInteriorRightWallEmissive",
		"PHPISideProjectionAlbedoHeight",
		"PHPISideProjectionNormalAo",
		"PHPISideProjectionEmissive",
		"PHPIFrontProjectionAlbedoHeight",
		"PHPIFrontProjectionNormalAo",
		"PHPIFrontProjectionEmissive",
		"PHPIBackProjectionAlbedoHeight",
		"PHPIBackProjectionNormalAo",
		"PHPIBackProjectionEmissive",
		"PHPITopProjectionAlbedoHeight",
		"PHPITopProjectionNormalAo",
		"PHPITopProjectionEmissive"*/
	)

    local matList = #(
        #Standard,					--1
        #Decal,						--2
        #Windshield,				--3
        #PortHole,					--4
        #Glass,						--5
        #GeoDecalFrosted,			--6
		#ClearCoat,					--7
        #ParallaxWindow,			--8
        #Anisotropic,				--9
        #Hair,						--10
        #SSS,						--11
        #Invisible,					--12
        #FakeTerrain,				--13
        #FresnelFade,				--14
        #EnvironmentOccluder,		--15
		#Ghost,						--16
		#GeoDecal_Dirt,				--17
		#Sail,						--18
		#Propeller,					--19
		#NotUsed1,					--20
		#Tree,						--21
		#Vegetation,				--22
		#Tire						--23
		--#PortHoleParallaxInterior	--24
    )

	local matListDisplayNames = #(
		"Standard",					--1
		"Decal",					--2
		"WindShield",				--3
		"PortHole",					--4
		"Glass",					--5
		"GeoDecal Frosted",			--6
		"ClearCoat",				--7
		"Parallax Window",			--8
		"Anisotropic",				--9
		"Hair",						--10
		"SSS",						--11
		"Invisible",				--12
		"Fake Terrain",				--13
		"Fresnel Fade",				--14
		"Environment Occluder",		--15
		"Ghost",					--16
		"GeoDecal BlendMasked",		--17
		"Sail",						--18
		"Propeller",				--19
		"",							--20 -- NotUsed1
		"Tree",						--21
		"Vegetation",				--22
		"Tire"						--23
		--"PortHole Parallax Interior"--24
	)
	
	local curPath = getFilenamePath (getSourceFileName())
	
	fn openBitmapGamma assetId gamma: =
	(
		local bm
		if gamma == unsupplied or (maxversion())[1] < 16000 then
			bm = openbitmap assetId
		else
			bm = openbitmap assetId gamma:gamma
		if bm != undefined then
			bm.filename = AssetManager.GetFileName assetId -- openbitmap return absolute path, set back to relative
		return bm
	)
	
	local TexBlack = openbitmap (pathConfig.appendPath curPath "MSFS2024Material_Black.bmp") 
	local TexWhite = openbitmap (pathConfig.appendPath curPath "MSFS2024Material_White.bmp") 
	local TexFlat = openbitmap (pathConfig.appendPath curPath "MSFS2024Material_Flat.bmp") gamma:1.0
	local TexGrey = openbitmap (pathConfig.appendPath curPath "MSFS2024Material_Grey.bmp") gamma:1.0
	local TexRadiance = openBitMap (pathConfig.appendPath curPath @"IBLmap\\Studio_Radiance.dds") gamma:1.0
	local TexIrradiance = openBitMap (pathConfig.appendPath curPath @"IBLmap\\Studio_Irradiance.dds") gamma:1.0
	local TexBRDFLUT = openBitMap (pathConfig.appendPath curPath "MSFS2024Material_BRDFLUT.png") gamma:1.0
	
	local filesTypes = "*.tif,*.dds,*.jpg,*.tga,*.png,*.bmp,*.hdr|*.tif;*.dds;*.jpg;*.tga;*.png;*.bmp;*.hdr"

	local clipboardClass = dotNetClass "System.Windows.Forms.Clipboard"
	
	local bApplyPhotometricScale = false
	
	fn fadeBitmap bm power:0.33 col:(color 102 102 102) =
	(
		local tempBm = bitmap bm.width bm.height color:col
		pasteBitmap tempBm bm [0,0] [0,0] type:#blend alphaMultiplier:power
	)

	fn mxs2dotBmp bm &dotbm width: height: =
	(
		local data = ""
		try (if clipboardClass.ContainsText() then data = clipboardClass.GetText()) catch()
		local w = if width != unsupplied then width else bm.width
		local h = w*bm.height/bm.width
		h = amax h 1
		if height != unsupplied then h = amin h height
		local tempBm = bitmap w h
		copy bm tempBm
		setClipboardBitmap tempBm
		free tempBm
		if dotbm != undefined then dotbm.dispose()
		try (dotbm = clipboardClass.GetImage()) catch()
		try (clipboardClass.SetText data) catch()
	)

	
	fn updateGlobalUI =
	(
		if ((MatEditor.mode == #basic and this==medit.GetCurMtl()) or
			(MatEditor.mode == #advanced and this==sme.GetMtlInParamEditor()))
		do
		(
			if loading == false and
				MatEditor.isOpen() and
				this.delegate != undefined then
			(
				this.texturesUI.updateUI()
				this.paramsUI.updateUI()
			)
		)		
	)
	fn updateTexturesUI =
	(
		if ((MatEditor.mode == #basic and this==medit.GetCurMtl()) or
			(MatEditor.mode == #advanced and this==sme.GetMtlInParamEditor()))
		do
		(
			if loading == false and
				MatEditor.isOpen() and
				this.delegate != undefined then
			(
				this.texturesUI.updateUI()
			)
		)
	)
	
	-- support paths relatifs
	fn getFullFilePath &filePath assetType:#Bitmap = FileResolutionManager.getFullFilePath filePath assetType
	
	-- get the name of the texture param from the delegate
	fn getDelTexPName basename =(
		"p_" + basename + "Tex"

	)
	
	--technique
	fn isFlag flag = findItem this.Flags flag > 0

	fn setShaderTechniqueByName techName= 
	(	
		/* 3dsmax strange bahviour : getTechniqueName and technique have indices starting from 1 and 0 respectivily*/
		
		local numTech = delegate.getNumberOfTechniques()
		-- format "number of technique is %\n" numTech
		for i=0 to (numTech-1) do
		(
			if delegate.getTechniqueName (i+1) == techName then
			(
				delegate.technique = i
				--format "set shader tech to %\n" (delegate.getTechniqueName i)
			)
			else
			(
				--format "cannot find technique from value %\n" i
			)
		)
	)

	fn createControllers =
	(
		-- instances of controllers on the delegate for the animatable params
		delegate.p_baseColorFactor.controller = this.baseColor.controller = bezier_point4 ()
		delegate.p_emissiveFactor.controller = this.emissive.controller = bezier_point4 ()
		delegate.p_roughnessFactor.controller = this.roughness.controller = bezier_float ()
		delegate.p_EmissiveMultiplierFactor.controller = this.emissiveMul.controller = bezier_float ()
		delegate.p_metallicFactor.controller = this.metallic.controller = bezier_float ()
		delegate.p_UVOffsetU.controller = this.UVOffsetU.controller = bezier_float ()
		delegate.p_UVOffsetV.controller = this.UVOffsetV.controller = bezier_float ()
		delegate.p_UVTilingU.controller = this.UVTilingU.controller = bezier_float ()
		delegate.p_UVTilingV.controller = this.UVTilingV.controller = bezier_float ()
		delegate.p_UVRotation.controller = this.UVRotation.controller = bezier_float ()
		delegate.p_wiperAnimState1.controller = this.wiperAnimState1.controller = bezier_float ()
		delegate.p_dirtAmount.controller = this.dirtBlendAmount.controller = bezier_float ()
		delegate.p_tireMudAnimState.controller = this.tireMudAnimState.controller = bezier_float ()
		delegate.p_tireDustAnimState.controller = this.tireDustAnimState.controller = bezier_float ()
	)
	
	fn loadControllers =
	(
		-- instances of controllers on the delegate for the animatable params
		if this.baseColor.controller == undefined then this.baseColor.controller = bezier_point4 ()
		if this.emissive.controller == undefined then this.emissive.controller = bezier_point4 ()
		if this.roughness.controller == undefined then this.roughness.controller = bezier_float ()
		if this.emissiveMul.controller == undefined then this.emissiveMul.controller = bezier_float ()
		if this.metallic.controller == undefined then this.metallic.controller = bezier_float ()
		if this.UVOffsetV.controller == undefined then this.UVOffsetV.controller = bezier_float ()
		if this.UVTilingU.controller == undefined then this.UVTilingU.controller = bezier_float ()
		if this.UVTilingV.controller == undefined then this.UVTilingV.controller = bezier_float ()
		if this.UVRotation.controller == undefined then this.UVRotation.controller = bezier_float ()
		if this.wiperAnimState1.controller == undefined then this.wiperAnimState1.controller = bezier_float ()
		if this.dirtBlendAmount.controller == undefined then this.dirtBlendAmount.controller = bezier_float ()
		if this.tireMudAnimState.controller == undefined then this.tireMudAnimState.controller = bezier_float ()
		if this.tireDustAnimState.controller == undefined then this.tireDustAnimState.controller = bezier_float ()
	)
	
	fn loadShader =
	(
		case (matList[this.materialType]) of
		(
			#Decal:
            (
                --format "SETTING DECAL \n"
				delegate.effectFile = pathConfig.appendPath curPath @"Fx/MSFS2024Material_Decal.fx"
				setShaderTechniqueByName("Tech_Decal")
            )
            #GeoDecalFrosted:
            (
                --format "SETTING DECAL \n"
				delegate.effectFile = pathConfig.appendPath curPath @"Fx/MSFS2024Material_Decal.fx"
				setShaderTechniqueByName("Tech_Decal")
				delegate.p_decalFrosted = true
            )
            #ParallaxWindow:
            (
				delegate.effectFile = pathConfig.appendPath curPath @"Fx/MSFS2024Material_ParallaxWindow.fx"
				setShaderTechniqueByName("Tech_Parallax")
            )
            #Invisible:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/MSFS2024Material_Flat.fx"
                setShaderTechniqueByName("Tech_Invisible")
            )
            #EnvironmentOccluder:
            (
                delegate.effectFile = pathConfig.appendPath curPath @"Fx/MSFS2024Material_Flat.fx"
                setShaderTechniqueByName("Tech_EnvOccluder")
            )

            default:
            (
				delegate.effectFile = pathConfig.appendPath curPath @"Fx/MSFS2024Material_Standard.fx"
				setShaderTechniqueByName("Tech_Base")
            )
		)
		delegate.p_materialType = this.materialType

		delegate.p_irradianceTex = TexIrradiance
		delegate.p_radianceTex = TexRadiance
		delegate.p_specularBRDF_LUT = TexBRDFLUT

		for i in TexList do
		(
			local propertyName = i + "Tex"
			if isProperty this propertyName then -- need to check weither property exists or not for removed ones.
			(
				if (getProperty this propertyName) == undefined then setProperty this (i + "Tex") ""
			)
		)
		
		-- format "loading shader % for % \n" matList[this.materialType] delegate.effectFile
	)
	
	parameters params rollout:paramsUI
	(		
		radianceMap  type:#filename assettype:#Bitmap
		irradianceMap type:#filename assettype:#Bitmap
	    uniqueInContainer type:#boolean default:false ui:uniqueInContainer animatable:false

		materialType type:#integer default:1 ui:materialType animatable:false
		
		baseColor type:#point4 default:white ui:BaseColor animatable:true
		emissive type:#point4 default:black ui:Emissive animatable:true

		dayNightCycle type:#boolean default:false ui:dayNightCycle animatable:false
		
		roughness type:#float default:1.0 ui:Roughness animatable:true
		emissiveMul type:#float default:1000.0 ui:emissiveMul animatable:true
		metallic type:#float default:1.0 ui:metallic animatable:true
		occlusionStrength type:#float default:1.0 ui:occlusionStrength animatable:false
		normalScale type:#float default:1.0 ui:normalScale animatable:false

		pearlescent type:#boolean default:false ui:pearlescent animatable:false
		pearlShift type:#float default:0.0 ui:pearlShift animatable:false
		pearlRange type:#float default:0.0 ui:pearlRange animatable:false
		pearlBrightness type:#float default:0.0 ui:pearlBrightness animatable:false

		iridescent type:#boolean default:false ui:iridescent animatable:false
		iridescentMinThickness type:#float default:100 ui:iridescentMinThickness animatable:false
		iridescentMaxThickness type:#float default:400 ui:iridescentMaxThickness animatable:false
		iridescentBrightness type:#float default:1.0 ui:iridescentBrightness animatable:false

		sailLightAbsorption type:#float default:1.0 ui:sailLightAbsorption animatable:false
		
		alphaMode type:#integer default:1 ui:alphaMode animatable:false
		drawOrder type:#integer default:0 ui:drawOrder animatable:false
		alphaCutoff type:#float default:0.5 ui:alphaCutoff animatable:false
		detailUVScale type:#float default:2.0 ui:detailUVScale animatable:false
		detailNormalScale type:#float default:1.0 ui:detailNormalScale animatable:false
		blendThreshold type:#float default:0.0 ui:blendThreshold animatable:false
		dirtUvScale type:#float default:1.0 ui:dirtUvScale animatable:false
		dirtBlendSharpness type:#float default:0.0 ui:dirtBlendSharpness animatable:false
		dirtBlendAmount type:#float default:0.0 ui:dirtBlendAmount animatable:true
		doubleSided type:#boolean default:false ui:doubleSided animatable:false

		
		decalColorFactor type:#float default:1.0 ui:decalColorFactor animatable:false
		decalRoughnessFactor type:#float default:1.0 ui:decalRoughnessFactor animatable:false
		decalMetalFactor type:#float default:1.0 ui:decalMetalFactor animatable:false
		decalOcclusionFactor type:#float default:1.0 ui:decalOcclusionFactor animatable:false
		decalNormalFactor type:#float default:1.0 ui:decalNormalFactor animatable:false
		decalEmissiveFactor type:#float default:1.0 ui:decalEmissiveFactor animatable:false
		decalRenderOnClearcoat type:#boolean default:false ui:decalRenderOnClearcoat animatable:false
		
		decalNormalOverrideFactor type:#float default:1.0 ui:decalNormalOverrideFactor animatable:false
		decalBlendSharpnessFactor type:#float default:1.0 ui:decalBlendSharpnessFactor animatable:false
		
		clearcoatRoughnessFactor type:#float default:1.0 ui:clearcoatRoughnessFactor animatable:false
		clearcoatNormalFactor type:#float default:1.0 ui:clearcoatNormalFactor animatable:false
		clearcoatColorRoughnessTiling type:#float default:1.0 ui:clearcoatColorRoughnessTiling animatable:false
		clearcoatNormalTiling type:#float default:1.0 ui:clearcoatNormalTiling animatable:false
		clearcoatInverseRoughness type:#boolean default:false ui:clearcoatInverseRoughness animatable:false
		clearcoatBaseRoughness type:#float default:0.5 ui:clearcoatBaseRoughness animatable:false

		parallaxScale type:#float default:0.0 ui:parallaxScale animatable:false
		roomSizeXScale type:#float default:0.5 ui:roomSizeXScale animatable:false
		roomSizeYScale type:#float default:0.5 ui:roomSizeYScale animatable:false
		roomNumberXY type:#float default:5.0 ui:roomNumberXY animatable:false
		corridor type:#boolean default:false ui:corridor animatable:false
		
		glassWidth type:#float default:0.0 animatable:false

		fresnelFactor type:#float default:1.0 ui:fresnelFactor animatable:false
		fresnelOpacityOffset type:#float default:0.0 ui:fresnelOpacityOffset animatable:false
		
		ghostBiasFactor type:#float default:1.0 ui:ghostBiasFactor animatable:false
		ghostPowerFactor type:#float default:0.0 ui:ghostPowerFactor animatable:false
		ghostScaleFactor type:#float default:0.0 ui:ghostScaleFactor animatable:false
		
		SSSColor type:#point4 default:white ui:SSSColor animatable:false

		collisionMaterial type:#boolean default:false ui:collisionMaterial animatable:false
		roadMaterial type:#boolean default:false ui:roadMaterial animatable:false
		disableMotionBlur type:#boolean default:false ui:disableMotionBlur animatable:false
		flipBackFace type:#boolean default:true ui:flipBackFace animatable:false
		noCastShadow type:#boolean default:false ui:noCastShadow animatable:false
		clampUVX type:#boolean default:false ui:clampUVX animatable:false
		clampUVY type:#boolean default:false ui:clampUVY animatable:false
		UVOffsetU type:#float default:0.0 ui:UVOffsetU animatable:true
		UVOffsetV type:#float default:0.0 ui:UVOffsetV animatable:true
		UVTilingU type:#float default:1.0 ui:UVTilingU animatable:true
		UVTilingV type:#float default:1.0 ui:UVTilingV animatable:true
		UVRotation type:#float default:0.0 ui:UVRotation animatable:true

		detail1Rough type:#float default:0.1 ui:detail1Rough animatable:false
		detail2Rough type:#float default:0.1 ui:detail2Rough animatable:false
		detail1Opacity type:#float default:0.5 ui:detail1Opacity animatable:false
		detail2Opacity type:#float default:0.5 ui:detail2Opacity animatable:false
		detailNormalRefractScale type:#float default:1.0 ui:detailNormalRefractScale animatable:false
		wiperAnimState1 type:#float default:0.0 ui:wiperAnimState1 animatable:true
		microScratchesTiling type:#float default:1.0 ui:microScratchesTiling animatable:false
		microScratchesStrength type:#float default:1.0 ui:microScratchesStrength animatable:false
		wiperLines type:#boolean default:true ui:wiperLines animatable:false
		wiperLinesTiling type:#float default:1.0 ui:wiperLinesTiling animatable:false
		wiperLinesStrength type:#float default:1.0 ui:wiperLinesStrength animatable:false

		canReceiveRain type:#boolean default:false ui:canReceiveRain animatable:false
		rainDropScale type:#float default:1.0 ui:rainDropScale animatable:false
		rainDropSide type:#boolean default:false ui:rainDropSide animatable:false

		tireMudNormalTiling type:#float default:1.0 ui:tireMudNormalTiling animatable:false
		tireMudAnimState type:#float default:0.0 ui:tireMudAnimState animatable:true
		tireDustAnimState type:#float default:0.0 ui:tireDustAnimState animatable:true

		-- Porthole parallax Interior
		/*PHPIRoomSizeX					type:#float		default:2.0		ui:spPHPIRoomSizeX					animatable:false
		PHPIRoomSizeY					type:#float		default:1.0		ui:spPHPIRoomSizeY					animatable:false
		PHPIRoomOffsetX					type:#float		default:0.0		ui:spPHPIRoomOffsetX				animatable:false
		PHPIRoomOffsetY					type:#float		default:0.0		ui:spPHPIRoomOffsetY				animatable:false
		PHPIRoomBackWallSizeOnTexture	type:#float		default:50.0	ui:spPHPIRoomBackWallSizeOnTexture	animatable:false --percent value
		PHPIProjectionRatio				type:#float		default:1.0		ui:spPHPIProjectionRatio			animatable:false
		PHPIProjectionSize				type:#float		default:80.0	ui:spPHPIProjectionSize				animatable:false --percent value
		PHPIProjectionSpacingX			type:#float		default:0.0		ui:spPHPIProjectionSpacingX			animatable:false --percent value
		PHPIMirrorLeftWall				type:#boolean	default:true	ui:chkPHPIMirrorLeftWall			animatable:false
		PHPIUseFront					type:#boolean	default:false	ui:chkPHPIUseFront					animatable:false
		PHPIUseBack						type:#boolean	default:false	ui:chkPHPIUseBack					animatable:false
		PHPIUseTop						type:#boolean	default:false	ui:chkPHPIUseTop					animatable:false*/

		guid type:#string default:"00000000-0000-0000-0000-000000000000" animatable:false

		debugWindshield_WiperMask type:#boolean default:false ui:debugWindshield_WiperMask animatable:false
		debugWindshield_InsectsAlbedo type:#boolean default:false ui:debugWindshield_InsectsAlbedo animatable:false
		debugWindshield_InsectsMask type:#float default:1.0 ui:debugWindshield_InsectsMask animatable:false

		on debugWindshield_WiperMask set val do		
		(
			animate off delegate.p_windshieldWiperMask = val
		)
		on debugWindshield_InsectsAlbedo set val do		
		(
			animate off delegate.p_windshieldInsectsAlbedo = val
		)
		on debugWindshield_InsectsMask set val do		
		(
			animate off delegate.p_windshieldInsectsMask = val
		)
		on debugWindshield_VertexColorRadio changed val do		
		(
			delegate.p_windshieldVertexColorR = false
			delegate.p_windshieldVertexColorR = false
			delegate.p_windshieldVertexColorR = false
			delegate.p_windshieldVertexColorR = false
			if val == 2 then
				animate off delegate.p_windshieldVertexColorR = true
			if val == 3 then
				animate off delegate.p_windshieldVertexColorG = true
			if val == 4 then
				animate off delegate.p_windshieldVertexColorB = true
			if val == 5 then
				animate off delegate.p_windshieldVertexColorA = true
		)

		on irradianceMap set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_irradianceTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_irradianceTex = TexIrradiance
		)

		on radianceMap set val do
		(
		    if val != undefined and getFullFilePath &val then
				delegate.p_radianceTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_radianceTex = TexRadiance
		)

		on baseColor set val do
		(
			if this.baseColor.controller!= undefined and delegate.p_baseColorFactor.controller != this.baseColor.controller  then
			(
				delegate.p_baseColorFactor.controller = this.baseColor.controller
			)
		)

		on roughness set val do
		(
			if this.roughness.controller!= undefined and delegate.p_roughnessFactor.controller != this.roughness.controller then
			(
				delegate.p_roughnessFactor.controller = this.roughness.controller
			)
		)

		on emissiveMul set val do
		(
			if this.emissiveMul.controller!= undefined and delegate.p_EmissiveMultiplierFactor.controller != this.emissiveMul.controller then
			(
				delegate.p_EmissiveMultiplierFactor.controller = this.emissiveMul.controller
			)
		)

		on metallic set val do
		(
			if this.metallic.controller!= undefined and delegate.p_metallicFactor.controller != this.metallic.controller then
			(
				delegate.p_metallicFactor.controller = this.metallic.controller
			)
		)
		on emissive set val do
		(
			if this.emissive.controller!= undefined and delegate.p_emissiveFactor.controller != this.emissive.controller then
			(
				delegate.p_emissiveFactor.controller = this.emissive.controller
			)
		)

		on occlusionStrength set val do
		(
			animate off delegate.p_occlusionStrength = val
		)
		
		on normalScale set val do
		(
			animate off delegate.p_normalScale = val
		)
		
		on alphaMode set val do
		(
			animate off delegate.p_alphaMode = this.alphaMode - 1
		)
		
		on drawOrder set val do
		(
			animate off delegate.p_drawOrder = val
		)
		
		on alphaCutoff set val do
		(
			animate off delegate.p_alphaCutoff = val
		)

		on UVOffsetU set val do
		(
			if this.UVOffsetU.controller != undefined and delegate.p_UVOffsetU.controller != this.UVOffsetU.controller then
			(
				delegate.p_UVOffsetU.controller = this.UVOffsetU.controller
			)
		)
		
		on UVOffsetV set val do
		(
			if this.UVOffsetV.controller != undefined and delegate.p_UVOffsetV.controller != this.UVOffsetV.controller then
			(
				delegate.p_UVOffsetV.controller = this.UVOffsetV.controller
			)
		)

		on UVTilingU set val do
		(
			if this.UVTilingU.controller != undefined and delegate.p_UVTilingU.controller != this.UVTilingU.controller then
			(
				delegate.p_UVTilingU.controller = this.UVTilingU.controller
			)
		)
		
		on UVTilingV set val do
		(
			if this.UVTilingV.controller != undefined and delegate.p_UVTilingV.controller != this.UVTilingV.controller then
			(
				delegate.p_UVTilingV.controller = this.UVTilingV.controller
			)
		)

		on UVRotation set val do
		(
			if this.UVRotation.controller != undefined and  delegate.p_UVRotation.controller != this.UVRotation.controller then
			(
				delegate.p_UVRotation.controller = this.UVRotation.controller
			)
		)

		on wiperAnimState1 set val do
		(
			if this.wiperAnimState1.controller != undefined and  delegate.p_wiperAnimState1.controller != this.wiperAnimState1.controller then
			(
				delegate.p_wiperAnimState1.controller = this.wiperAnimState1.controller
			)
		)

		on tireMudAnimState set val do
		(
			if this.tireMudAnimState.controller != undefined and  delegate.p_tireMudAnimState.controller != this.tireMudAnimState.controller then
			(
				delegate.p_tireMudAnimState.controller = this.tireMudAnimState.controller
			)
		)
		
		on tireDustAnimState set val do
		(
			if this.tireDustAnimState.controller != undefined and  delegate.p_tireDustAnimState.controller != this.tireDustAnimState.controller then
			(
				delegate.p_tireDustAnimState.controller = this.tireDustAnimState.controller
			)
		)

		-- disable because of missing variable in shader
		-- TODO : find why
		-- on tireMudNormalTiling set val do
		-- (
		-- 	animate off delegate.p_tireMudNormalTiling = val
		-- )
		
		on detailUVScale set val do
		(
			animate off delegate.p_detailUVScale = val
		)
		
		on detailUVOffsetX set val do
		(
			animate off delegate.p_detailUVOffsetX = val
		)
		
		on detailUVOffsetY set val do
		(
			animate off delegate.p_detailUVOffsetY = val
		)
		
		on detailNormalScale set val do
		(
			animate off delegate.p_detailNormalScale = val
		)
		
		on blendThreshold set val do
		(
			animate off delegate.p_blendThreshold = val
		)
		
		on glassWidth set val do
		(
			animate off delegate.p_glassWidth = val
		)
		
		on fresnelFactor set val do
		(
			animate off delegate.p_fresnelFactor = val
		)
		
		on fresnelOpacityOffset set val do
		(
			animate off delegate.p_fresnelOpacityOffset = val
		)
		
-- 		on ghostPowerFactor set val do
-- 		(
-- 			animate off delegate.p_ghostPowerFactor = val
-- 		)

-- 		on ghostBiasFactor set val do
-- 		(
-- 			animate off delegate.p_ghostBiasFactor = val
-- 		)

-- 		on ghostScaleFactor set val do
-- 		(
-- 			animate off delegate.p_ghostScaleFactor = val
-- 		)
		
		on parallaxScale set val do
		(
			animate off delegate.p_parallaxScale = val
		)
		
		on roomSizeXScale set val do
		(
			animate off delegate.p_roomSizeXScale = val
		)
		
		on roomSizeYScale set val do
		(
			animate off delegate.p_roomSizeYScale = val
		)
		
		on roomNumberXY set val do
		(
			animate off delegate.p_roomNumberXY = val
		)

		on corridor set val do
		(
			animate off delegate.p_corridorEnabled = val
		)
		
		on SSSColor set val do
		(
			animate off delegate.p_SSSColorFactor = val
		)
		
		on pearlescent set val do 
		(			
			animate off delegate.p_pearlescentEnabled = val
		) 
				
		on pearlRange set val do 
		(			
			animate off delegate.p_pearlRange = val
		) 
				
		on pearlShift set val do 
		(			
			animate off delegate.p_pearlShift = val
		) 

		on pearlBrightness set val do 
		(			
			animate off delegate.p_pearlBrightness = val
		)

		on iridescent set val do 
		(			
			animate off delegate.p_iridescentEnabled = val
		)

		on iridescentMinThickness set val do 
		(			
			animate off delegate.p_iridescentMinThickness = val
		)

		on iridescentMaxThickness set val do 
		(			
			animate off delegate.p_iridescentMaxThickness = val
		)

		on iridescentBrightness set val do 
		(			
			animate off delegate.p_iridescentBrightness = val
		)

		on sailLightAbsorption set val do 
		(			
			animate off delegate.p_sailLightAbsorption = val
		)

		on dirtBlendAmount set val do
		(
			if this.dirtBlendAmount.controller != undefined and delegate.p_dirtAmount.controller != this.dirtBlendAmount.controller then
			(
				delegate.p_dirtAmount.controller = this.dirtBlendAmount.controller
			)
		)

		on dirtBlendSharpness set val do
		(			
			animate off delegate.p_dirtBlendSharpness = val
		)

		on dirtUvScale set val do
		(			
			animate off delegate.p_dirtUvScale = val
		)

		-- Porthole parallax Interior
		/*on PHPIMirrorLeftWall	set val do updateTexturesUI()
		on PHPIUseFront			set val do updateTexturesUI()
		on PHPIUseBack			set val do updateTexturesUI()
		on PHPIUseTop			set val do updateTexturesUI()*/
	)
	
	parameters textures rollout:texturesUI
	(
		texSlotSize type:#integer default:2 ui:texSlotSize animatable:false --keep user choice for tex slots size UI display
		
		-- Dev note: if adding bitmap slot, XML export will not "see" textures until they are actually USED for something (usedMaps fn), ie bitmap has been opened somehow (here mostly opened for delegate shader)
		BaseColorTex							type:#filename assettype:#Bitmap
		OcclusionRoughnessMetallicTex			type:#filename assettype:#Bitmap
		NormalTex								type:#filename assettype:#Bitmap
		WetnessAOTex							type:#filename assettype:#Bitmap
		WindshieldDetailNormalTex				type:#filename assettype:#Bitmap
		AnisoDirectionRoughnessTex				type:#filename assettype:#Bitmap
		OpacityTex								type:#filename assettype:#Bitmap --named like the sampler in engine side (for SSS)
		DirtTex									type:#filename assettype:#Bitmap
		DirtOcclusionRoughnessMetallicTex		type:#filename assettype:#Bitmap
		EmissiveTex								type:#filename assettype:#Bitmap
		DetailColorTex							type:#filename assettype:#Bitmap
		DetailOcclusionRoughnessMetallicTex		type:#filename assettype:#Bitmap
		DetailNormalTex							type:#filename assettype:#Bitmap
		BlendMaskTex							type:#filename assettype:#Bitmap
		FoliageMaskTex							type:#filename assettype:#Bitmap
		OcclusionTex							type:#filename assettype:#Bitmap
		ClearcoatColorRoughnessTex				type:#filename assettype:#Bitmap
		ClearcoatNormalTex						type:#filename assettype:#Bitmap
		ScratchesNormalTex						type:#filename assettype:#Bitmap
		WiperMaskTex							type:#filename assettype:#Bitmap
		IridescentThicknessTex					type:#filename assettype:#Bitmap
		WindshieldInsectsTex					type:#filename assettype:#Bitmap
		WindshieldInsectsMaskTex				type:#filename assettype:#Bitmap
		TireDetailsTex							type:#filename assettype:#Bitmap
		TireMudNormalTex						type:#filename assettype:#Bitmap
		-- Porthole parallax Interior
		/*PHPIInteriorHallwayAlbedoTex			type:#filename assettype:#Bitmap
		PHPIInteriorHallwayNormalAoTex			type:#filename assettype:#Bitmap
		PHPIInteriorHallwayEmissiveTex			type:#filename assettype:#Bitmap
		PHPIInteriorLeftWallAlbedoTex			type:#filename assettype:#Bitmap
		PHPIInteriorLeftWallNormalAoTex			type:#filename assettype:#Bitmap
		PHPIInteriorLeftWallEmissiveTex			type:#filename assettype:#Bitmap
		PHPIInteriorRightWallAlbedoTex			type:#filename assettype:#Bitmap
		PHPIInteriorRightWallNormalAoTex		type:#filename assettype:#Bitmap
		PHPIInteriorRightWallEmissiveTex		type:#filename assettype:#Bitmap
		PHPISideProjectionAlbedoHeightTex		type:#filename assettype:#Bitmap
		PHPISideProjectionNormalAoTex			type:#filename assettype:#Bitmap
		PHPISideProjectionEmissiveTex			type:#filename assettype:#Bitmap
		PHPIFrontProjectionAlbedoHeightTex		type:#filename assettype:#Bitmap
		PHPIFrontProjectionNormalAoTex			type:#filename assettype:#Bitmap
		PHPIFrontProjectionEmissiveTex			type:#filename assettype:#Bitmap
		PHPIBackProjectionAlbedoHeightTex		type:#filename assettype:#Bitmap
		PHPIBackProjectionNormalAoTex			type:#filename assettype:#Bitmap
		PHPIBackProjectionEmissiveTex			type:#filename assettype:#Bitmap
		PHPITopProjectionAlbedoHeightTex		type:#filename assettype:#Bitmap
		PHPITopProjectionNormalAoTex			type:#filename assettype:#Bitmap
		PHPITopProjectionEmissiveTex			type:#filename assettype:#Bitmap*/
		
		-- filenames
		on BaseColorTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_baseColorTex = openBitmapGamma val gamma:2.2
				delegate.p_baseColorEnabled = true
			)	
			else
			(
				delegate.p_baseColorTex = TexWhite
				delegate.p_baseColorEnabled = false
			)
				
		)

		on OcclusionRoughnessMetallicTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_occlusionRoughnessMetallicTex = openBitmapGamma val gamma:1.0
				delegate.p_occRoughMetalEnabled = true
			)
			else
			(
				delegate.p_occlusionRoughnessMetallicTex = TexWhite
				delegate.p_occRoughMetalEnabled = false
			)
		)
		
		on NormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_normalTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_normalTex = TexFlat
		)
		
		on WetnessAOTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_wetnessAOTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_wetnessAOTex = TexFlat
		)

		on WindshieldDetailNormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_windshieldDetailNormalTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_windshieldDetailNormalTex = TexFlat
		)

		on ScratchesNormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_scratchesNormalTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_scratchesNormalTex = TexFlat
		)

		on WiperMaskTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_wiperMaskTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_wiperMaskTex = TexBlack
		)

		on IridescentThicknessTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_iridescentThicknessTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_iridescentThicknessTex = TexBlack
		)

		on WindshieldInsectsTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_windshieldInsectsTex = openBitmapGamma val gamma:1.0
				delegate.p_windshieldInsectsEnabled = true
			)
			else
			(
				delegate.p_windshieldInsectsTex = TexBlack
				delegate.p_windshieldInsectsEnabled = false
			)
		)

		on WindshieldInsectsMaskTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_windshieldInsectsMaskTex = openBitmapGamma val gamma:1.0
				delegate.p_windshieldInsectsMaskEnabled = true
			)
			else
			(
				delegate.p_windshieldInsectsMaskTex = TexBlack
				delegate.p_windshieldInsectsMaskEnabled = false
			)
		)

		on AnisoDirectionRoughnessTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_anisoDirectionRoughnessTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_anisoDirectionRoughnessTex = TexFlat
		)
		
		on DirtTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_dirtTex = openBitmapGamma val gamma:1.0
				delegate.p_dirtEnabled = true
				delegate.p_dirtUVScale = dirtUVScale
				delegate.p_dirtAmount = dirtBlendAmount
				delegate.p_dirtBlendSharpness = dirtBlendSharpness
			)
			else
			(
				delegate.p_dirtTex = TexGrey
				delegate.p_dirtEnabled = false
			)
		)

		on DirtOcclusionRoughnessMetallicTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_dirtOccRoughMetalTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_dirtOccRoughMetalTex = TexGrey
		)
		
		on OpacityTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_opacityTex = openBitmapGamma val gamma:1.0
			else
				delegate.p_opacityTex = TexFlat
		)
		
		on EmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
				delegate.p_emissiveTex = openBitmapGamma val gamma:2.2
			else
				delegate.p_emissiveTex = TexBlack
		)
		
		on DetailColorTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_detailColorTex = openBitmapGamma val gamma:1.0
				delegate.p_detailColorEnabled = true
			)
			else
			(
				delegate.p_detailColorTex = TexGrey
				delegate.p_detailColorEnabled = false
			)
		)
		
		on DetailOcclusionRoughnessMetallicTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_detailOcclusionRoughnessMetallicTex = openBitmapGamma val gamma:1.0
				delegate.p_detailOccRoughMetalEnabled = true
			)
			else
			(
				delegate.p_detailOcclusionRoughnessMetallicTex = TexWhite
				delegate.p_detailOccRoughMetalEnabled = false
			)
		)
		
		on DetailNormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_detailNormalTex = openBitmapGamma val gamma:1.0
				delegate.p_detailNormalEnabled = true
			)
			else
			(
				delegate.p_detailNormalTex = TexFlat
				delegate.p_detailNormalEnabled = false
			)
		)
		
		on BlendMaskTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_blendMaskTex = openBitmapGamma val gamma:1.0
				delegate.p_blendmaskEnabled = true
			)
			else
			(
				delegate.p_blendMaskTex = TexBlack
				delegate.p_blendmaskEnabled = false
			)
		)

		on FoliageMaskTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_foliageMaskTex = openBitmapGamma val gamma:1.0
				delegate.p_foliagemaskEnabled = true
			)
			else
			(
				delegate.p_foliageMaskTex = TexBlack
				delegate.p_foliagemaskEnabled = false
			)
		)
		
		on OcclusionTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_occlusionTex = openBitmapGamma val gamma:1.0
				delegate.p_occlusionEnabled = true
			)
			else
			(
				delegate.p_occlusionTex = TexWhite
				delegate.p_occlusionEnabled = false
			)
		)

		on ClearcoatColorRoughnessTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_clearcoatColorRoughnessTex = openBitmapGamma val gamma:1.0
				delegate.p_clearcoatColorRoughnessEnabled = true
			)
			else
			(
				delegate.p_clearcoatColorRoughnessTex = TexBlack
				delegate.p_clearcoatColorRoughnessEnabled = false
			)
		)

		on ClearcoatNormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_clearcoatNormalTex = openBitmapGamma val gamma:1.0
				delegate.p_clearcoatNormalEnabled = true
			)
			else
			(
				delegate.p_clearcoatNormalTex = TexFlat
				delegate.p_clearcoatNormalEnabled = false
			)
		)

		on TireDetailsTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_tireDetailsTex = openBitmapGamma val gamma:1.0
				delegate.p_tireDetailsEnabled = true
			)
			else
			(
				delegate.p_tireDetailsTex = TexWhite
				delegate.p_tireDetailsEnabled = false
			)
		)

		on TireMudNormalTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_tireMudNormalTex = openBitmapGamma val gamma:1.0
				delegate.p_tireMudNormalEnabled = true
			)
			else
			(
				delegate.p_tireMudNormalTex = TexBlack
				delegate.p_tireMudNormalEnabled = false
			)
		)

		-- Porthole parallax interior
		/*on PHPIInteriorHallwayAlbedoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorHallwayAlbedoTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiInteriorHallwayAlbedoTex = TexBlack
			)
		)
		on PHPIInteriorHallwayNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorHallwayNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiInteriorHallwayNormalAoTex = TexBlack
			)
		)
		on PHPIInteriorHallwayEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorHallwayEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiInteriorHallwayEmissiveTex = TexBlack
			)
		)

		on PHPIInteriorLeftWallAlbedoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorLeftWallAlbedoTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiInteriorLeftWallAlbedoTex = TexBlack
			)
		)
		on PHPIInteriorLeftWallNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorLeftWallNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiInteriorLeftWallNormalAoTex = TexBlack
			)
		)
		on PHPIInteriorLeftWallEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorLeftWallEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiInteriorLeftWallEmissiveTex = TexBlack
			)
		)

		on PHPIInteriorRightWallAlbedoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorRightWallAlbedoTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiInteriorRightWallAlbedoTex = TexBlack
			)
		)
		on PHPIInteriorRightWallNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorRightWallNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiInteriorRightWallNormalAoTex = TexBlack
			)
		)
		on PHPIInteriorRightWallEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiInteriorRightWallEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiInteriorRightWallEmissiveTex = TexBlack
			)
		)

		on PHPISideProjectionAlbedoHeightTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiSideProjectionAlbedoHeightTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiSideProjectionAlbedoHeightTex = TexBlack
			)
		)
		on PHPISideProjectionNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiSideProjectionNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiSideProjectionNormalAoTex = TexBlack
			)
		)
		on PHPISideProjectionEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiSideProjectionEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiSideProjectionEmissiveTex = TexBlack
			)
		)

		on PHPIFrontProjectionAlbedoHeightTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiFrontProjectionAlbedoHeightTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiFrontProjectionAlbedoHeightTex = TexBlack
			)
		)
		on PHPIFrontProjectionNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiFrontProjectionNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiFrontProjectionNormalAoTex = TexBlack
			)
		)
		on PHPIFrontProjectionEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiFrontProjectionEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiFrontProjectionEmissiveTex = TexBlack
			)
		)

		on PHPIBackProjectionAlbedoHeightTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiBackProjectionAlbedoHeightTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiBackProjectionAlbedoHeightTex = TexBlack
			)
		)
		on PHPIBackProjectionNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiBackProjectionNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiBackProjectionNormalAoTex = TexBlack
			)
		)
		on PHPIBackProjectionEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiBackProjectionEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiBackProjectionEmissiveTex = TexBlack
			)
		)

		on PHPITopProjectionAlbedoHeightTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiTopProjectionAlbedoHeightTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiTopProjectionAlbedoHeightTex = TexBlack
			)
		)
		on PHPITopProjectionNormalAoTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiTopProjectionNormalAoTex = openBitmapGamma val gamma:1.0
			)
			else
			(
				delegate.p_phpiTopProjectionNormalAoTex = TexBlack
			)
		)
		on PHPITopProjectionEmissiveTex set val do
		(
			if val != undefined and getFullFilePath &val then
			(
				delegate.p_phpiTopProjectionEmissiveTex = openBitmapGamma val gamma:2.2
			)
			else
			(
				delegate.p_phpiTopProjectionEmissiveTex = TexBlack
			)
		)*/
	)
	
	rollout paramsUI "Parameters"
	(
		local uiScale = MSFS2024_getUiScale()
		
		local maxWidth = paramsUI.width - 26
		local halfMaxWidth = maxWidth * 0.5
		local leftFrameWidth = halfMaxWidth - 10
		local rightFrameWidth = halfMaxWidth - 10
		local rightFrameOffset = 10
		
		-- Permanent visible boxes
        checkbox uniqueInContainer "Avoid duplicate materials when using containers" offset:[0,0] align:#left \
			tooltip:"Avoid duplicate material when using duplicated container\nDoesn't work with multi-materials !"
		
		groupbox lineSep1 "" width:maxwidth height:2
		
		label materialTypeLab "Material Type:" across:2 offset:[0,3+3] align:#left
		dropdownlist materialType "" items:matListDisplayNames offset:[0,3] width:(maxWidth*0.75) align:#right
		
		button chart "Color chart reference" offset:[0,0] align:#left across:2 tooltip:"Color chart reference" \
			iconName:@"MaterialEditor\VideoColorCheck" iconSize:[16, 16] height:20 width:30
-- 			iconName:@"PolyTools\ViewportCanvas\ColorPalette" iconSize:[43, 16] height:20 width:47
		button emissionCalc "Emissive calculator" offset:[0,0] align:#right tooltip:"Emissive calculator" \
			iconName:@"CommandPanel\Modify\ConfigureModifierSets" iconSize:[16, 16] height:20 width:30
		
		colorpicker baseColor "Albedo:" modal:false fieldWidth:40 height:20 align:#left offset:[0,0] across:4 \
			tooltip:"The RGBA components of the base color of the material. The fourth component (A) is the alpha coverage of the material. The alphaMode property specifies how alpha is interpreted. These values are linear. If a baseColorTexture is specified, this value is multiplied with the texel values."
		colorpicker emissive "Emission:" modal:false fieldWidth:40 height:20 align:#right offset:[50,0] \
			tooltip:"The RGB components of the emissive color of the material. These values are linear. If an emissiveTexture is specified, this value is multiplied with the texel values."
		spinner emissiveMul "x " range:[0,1000000,1000] scale:1 fieldWidth:55 align:#right offset:[48,2] \
			tooltip:"Emssion intensity in Candela per square meter"
		label emissionUnitLab "cd/m\xB2" offset:[0,3] align:#right
		
		groupBox alphaModeBox "Alpha Mode:" height:80 width:leftFrameWidth offset:[0,5]
		radioButtons alphaMode "" labels:#("OPAQUE","MASK","BLEND","DITHER") columns:1 align:#left offset:[10,-70] \
			tooltip:#(
				"OPAQUE - The rendered output is fully opaque and any alpha value is ignored.",
				"MASK - The rendered output is either fully opaque or fully transparent depending on the alpha value and the specified alpha cutoff value. This mode is used to simulate geometry such as tree leaves or wire fences.",
				"BLEND - The rendered output is combined with the background using the normal painting operation (i.e. the Porter and Duff over operator). This mode is used to simulate geometry such as guaze cloth or animal fur.",
				"DITHER - The rendered output is blend with dithering dot pattern"
				)

		groupBox renderFlagBox "Render Param:" height:140 width:leftFrameWidth offset:[0,10]
		spinner drawOrder "Draw Order:" type:#integer range:[-999,999,0] fieldWidth:30 offset:[10,-128] align:#left\
			tooltip:"Draw Order Offset, to manually sort decals draw order for example"
		checkbox noCastShadow "Don't cast shadows" offset:[10,0] align:#left \
			tooltip:"Don't cast shadows"
		checkbox doubleSided "Double Sided" offset:[10,0] align:#left \
			tooltip:"The doubleSided property specifies whether the material is double sided. When this value is false, back-face culling is enabled. When this value is true, back-face culling is disabled and double sided lighting is enabled. The back-face must have its normals reversed before the lighting equation is evaluated."
		checkbox dayNightCycle "Day Night Cycle" offset:[10,0] align:#left \
			tooltip:"The emissive will be related to the ingame Day Night Cycle. When this value is false the emissive is Always ON."
		checkbox disableMotionBlur "Disable Motion Blur" offset:[10,0] align:#left \
		tooltip:"When this value is ON, the MotionBlur is disabled on the material, no matter what is defined in graphic options"
		checkbox flipBackFace "Flip BackFace Normal" offset:[10,0] align:#left \
		tooltip:"When this value is ON, the back face normal will be flipped. This is useful to make translucent material."

		--groupBox usualMaterialBox "material param:" height:250 width:200
		spinner metallic "Metallic:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[0,-220] \
			tooltip:"The metalness of the material. A value of 1.0 means the material is a metal. A value of 0.0 means the material is a dielectric. Values in between are for blending between metals and dielectrics such as dirty metallic surfaces. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the metallic texel values."
		spinner roughness "Roughness:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right
			tooltip:"The roughness of the material. A value of 1.0 means the material is completely rough. A value of 0.0 means the material is completely smooth. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the roughness texel values."
		spinner occlusionStrength "AO Strength:" range:[0,2,1] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"The occlusion strength applied to each pixel of the texture. A value of 0.0 means no occlusion. A value of 1.0 means texture occlusion ,A value of 2.0 means complete occlusion, if no texture is specified the default AO texture is white"
		label reflectionMaskLabel "Reflection Mask:" offset:[-50,-19] align:#right
		spinner normalScale "Normal Strength:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"The scalar multiplier applied to each normal vector of the normal texture. This value is ignored if normalTexture is not specified."
		spinner alphaCutoff "Alpha Cutoff:" range:[0,1,1] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"When alphaMode is set to MASK the alphaCutoff property specifies the cutoff threshold. If the alpha value is greater than or equal to the alphaCutoff value then it is rendered as fully opaque, otherwise, it is rendered as fully transparent. alphaCutoff value is ignored for other modes."
		spinner detailUVScale "Detail UV Tiling:" range:[0.01,100,2] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"The tiling size of the detail UV texture."
		spinner detailNormalScale "Detail Normal Strength:" range:[0.00,1.00,1.0] scale:0.01 fieldWidth:40 align:#bottomright \
			tooltip:"The scalar multiplier applied to each normal vector of the detail normal texture. This value is ignored if detailNormalTexture is not specified."
		spinner blendThreshold "Detail Threshold:" range:[0.001,1.000,0.100] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Blend Threshold need blendMask Tex"
		spinner dirtUvScale "Wear Overlay UV Scale:" range:[0.001,10.000,1.000] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"UV Scale of the Wear overlay"
		spinner dirtBlendSharpness "Wear Blend Sharpness:" range:[0.0,1.000,0.0] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Allows the use of blend sharpness with the Wear Overlay texture's alpha"
		spinner dirtBlendAmount "Wear Amount:" range:[0.0,1.000,1.000] scale:0.01 fieldWidth:40 align:#right \
			tooltip:"Blend strength of Wear overlay"
		
		groupBox gameplayBox "Gameplay Param:" height:80 width:leftFrameWidth offset:[0,0]
		checkbox collisionMaterial "Collision Material" offset:[10,-80+12] align:#left tooltip:"Collision Material"
		checkbox roadMaterial "Road Collision Material" offset:[10,0] align:#left tooltip:"Road Collision Material"

		groupBox rainBox "Rain Param:" height:80 width:rightFrameWidth offset:[(halfMaxWidth+rightFrameOffset),-57]
		checkbox canReceiveRain "Receive Rain" offset:[(halfMaxWidth+rightFrameOffset+10),-68] align:#left tooltip:"Determine if surface can receive rain on it"
		spinner rainDropScale "Rain Drop Tiling:" range:[0,100,1] scale:1 fieldWidth:40 offset:[(halfMaxWidth+rightFrameOffset+10), 0] align:#left tooltip:"Rain Drop Tiling"
		checkbox rainDropSide "Rain on BackFace" offset:[(halfMaxWidth+rightFrameOffset+10), 0] align:#left tooltip:"Determine on which side of the surface the rain will drop"

		groupBox UVParams "UV:" height:90 width:maxWidth offset:[0,10]
		spinner UVOffsetU "Offset U:" range:[-10.00,10.00,0.0] scale:0.01  offset:[8, -75] fieldWidth:40 align:#left tooltip:"UV Offset U" across:3
		spinner UVTilingU "Tiling U:" range:[-10.00,10.00,1.0] scale:0.01 offset:[0, -75] fieldWidth:40 align:#left tooltip:"UV Tiling U"
		checkbox clampUVX "Clamp U" offset:[0,-75] align:#left
		spinner UVOffsetV "Offset V:" range:[-10.00,10.00,0.0] scale:0.01 offset:[8, 0] fieldWidth:40 align:#left tooltip:"UV Offset V" across:3
		spinner UVTilingV "Tiling V:" range:[-10.00,10.00,1.0] scale:0.01 offset:[0, 0] fieldWidth:40 align:#left tooltip:"UV Tiling V"
		checkbox clampUVY "Clamp V" offset:[0,0] across:2 align:#left
		spinner UVRotation "Rotation:" range:[-360.00,360.00,0.0] scale:0.01 offset:[8, 0] fieldWidth:40 align:#left tooltip:"UV Rotation"		

		-- Potentially not visible boxes
		local posY = 540

		groupBox decalBox "Decal per component blend factors:" height:125 width:maxWidth pos:[13,posY]
		spinner decalColorFactor "Color:" 					range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-20,-110] across:2
		spinner decalRoughnessFactor "Roughness:" 	range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-60,-110]
		spinner decalMetalFactor "Metal:" 					range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-20,0] across:2
		spinner decalOcclusionFactor "Occlusion:" 		range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-60,0]
		spinner decalNormalFactor "Normal:" 				range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-20,0] across:2
		spinner decalEmissiveFactor "Emissive:" 			range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-60,0]
		spinner decalNormalOverrideFactor "Normal Mode Tangent/Override:" 	range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-60,0]
		spinner decalBlendSharpnessFactor "Blend Sharpness:" 	range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-60,0]
		checkbox decalRenderOnClearcoat "Render on ClearCoat" align:#left offset:[10, -20] tooltip:"Render decal on top of ClearCoat"

		groupBox TireBox "Tire parameters:" height:86 width:maxWidth pos:[13,posY]
		spinner tireMudNormalTiling "Mud Tiling:" range:[0,100.0,0] scale:0.1 fieldWidth:40 offset:[10, -70] align:#left across:1 tooltip:"Tire Mud Normal Tiling"
		spinner tireMudAnimState "Mud Anim State:" range:[0,1,0] scale:0.01 fieldWidth:40 offset:[10, 0] align:#left across:1 tooltip:"Tire Mud Animation State"
		spinner tireDustAnimState "Dust Anim State:" range:[0,1,0] scale:0.01 fieldWidth:40 offset:[10, 0] align:#left across:1 tooltip:"Tire Dust Animation State"

		groupBox clearcoatBox "ClearCoat Param:" height:130 width:maxWidth pos:[13,posY]
		spinner clearcoatRoughnessFactor "Clearcoat Roughness Factor " range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-15,-115]
		spinner clearcoatNormalFactor "Clearcoat Normal Factor " range:[0,1,1] scale:0.01 fieldWidth:40 align:#right offset:[-15,0]
		spinner clearcoatColorRoughnessTiling "Clearcoat Color/Roughness Tiling " range:[-1000,1000,1] scale:0.01 fieldWidth:40 align:#right offset:[-15,0]
		spinner clearcoatNormalTiling "Clearcoat Normal Tiling " range:[-1000,1000,1] scale:0.01 fieldWidth:40 align:#right offset:[-15,0]
		checkbox clearcoatInverseRoughness "Not use clearcoat texture" align:#left offset:[10, 0] across:2 tooltip:"Use the roughness in the comp slot as the roughness used for the clearcoat layer"
		spinner clearcoatBaseRoughness "Base Roughness" range:[0,1,0.1] scale:0.01 fieldWidth:40 align:#right offset:[-15,0] tooltip:"Roughness used to for the base layer, under the clearcoat layer"

		groupBox SSSbox "SSS parameters:" height:50 width:maxWidth pos:[13,posY]
		colorpicker SSSColor "SSS Color" modal:false fieldWidth:30 height:20 align:#left offset:[10,-35] \
			tooltip:"The RGBA components of the SSS color of the material. These values are linear. If a SSSTexture is specified, this value is multiplied with the texel values."
		
		groupBox GlassBox "Glass Width:" height:64 width:maxWidth pos:[13,posY]
		spinner glassWidthUI "Glass Width (mm): " range:[0.000,1000.000,0.000] scale:1 fieldWidth:40 offset:[-80, -52] align:#right \
			tooltip:"Glass Deformation Factor"
		
		groupBox ParallaxBox "Parallax parameters:" height:130 width:maxWidth pos:[13,posY]
		spinner parallaxScale "Parallax scale:" range:[0.000,1.000,0.500] scale:0.01 fieldWidth:40 offset:[10, -115] align:#left \
			tooltip:"Parallax scale"
		spinner roomSizeXScale "room SizeX Scale:" range:[0.01,10.000,0.500] scale:0.01 fieldWidth:40 offset:[10, 0] align:#left \
			tooltip:"room SizeX Scale"
		spinner roomSizeYScale "room SizeY Scale:" range:[0.01,10.000,0.500] scale:0.01 fieldWidth:40 offset:[10, 0] align:#left \
			tooltip:"room SizeY Scale"
		spinner roomNumberXY "room number XY:" range:[1,16,2] scale:1 fieldWidth:40 offset:[10, 0] align:#left \
			tooltip:"room Number XY"
		checkbox corridor "Corridor" offset:[10, 0] align:#left tooltip:"Use as a corridor"

		groupBox fresnelBox "Fresnel parameters:" height:70 width:maxWidth pos:[13,posY]
		spinner fresnelFactor "Fresnel Factor:" range:[0.001,100.000,1.000] scale:0.01 fieldWidth:40 offset:[-80,-55] align:#right \
			tooltip:"Fresnel Factor"
		spinner fresnelOpacityOffset "Fresnel Opacity Bias:" range:[-1.0,1.0,0.000] scale:0.01 fieldWidth:40 offset:[-80, 0] align:#right \
			tooltip:"Fresnel Opacity Bias"
			
		groupBox ghostBox "Ghost parameters:" height:80 width:maxWidth pos:[13,posY]
		spinner ghostBiasFactor "Bias Factor:" range:[0.001,64.000,1.000] scale:0.01 fieldWidth:40 offset:[-80,-70] align:#right \
			tooltip:"Ghost Bias Factor"
		spinner ghostPowerFactor "Ghost Power:" range:[0.0,1.0,0.000] scale:0.01 fieldWidth:40 offset:[-80, 0] align:#right \
			tooltip:"Ghost Power Factor"
		spinner ghostScaleFactor "Ghost Scale:" range:[0.0,1.0,1.000] scale:0.01 fieldWidth:40 offset:[-80, 0] align:#right \
			tooltip:"Ghost Scale Factor"
			
		groupBox pearlBox "Pearl Param:" height:100 width:maxWidth pos:[13,posY]
		checkbox pearlescent "Use Pearl Effect" offset:[10,-90] align:#left \
			tooltip:"Enables Pearl effect on reflections"
		spinner pearlShift "Color Shift" range:[-999,999,0] offset:[10,0] fieldWidth:30 align:#left \
			tooltip:"Color Shift"
		spinner pearlRange "Color Range" range:[-999,999,0] offset:[10,0] fieldWidth:30 align:#left \
			tooltip:"Color Range"
		spinner pearlBrightness "Color Brightness" range:[-1,1,0] offset:[10,0] fieldWidth:30 align:#left \
			tooltip:"Color Brightness"

		groupBox iridescentBox "Iridescent Param:" height:100 width:maxWidth pos:[13,posY]
		checkbox iridescent "Use Iridescence" offset:[10,-90] align:#left \
			tooltip:"Enables Iridescence"
		spinner iridescentMinThickness "Min Thickness" range:[0,2000,0] offset:[10,0] fieldWidth:50 align:#left \
			tooltip:"Iridescent Min Thickness"
		spinner iridescentMaxThickness "Max Thickness" range:[0,2000,0] offset:[10,0] fieldWidth:50 align:#left \
			tooltip:"Iridescent Max Thickness"
		spinner iridescentBrightness "Brightness" range:[0,10,0] offset:[10,0] fieldWidth:30 align:#left \
			tooltip:"Iridescent Brightness"

		groupBox sailBox "Sail Parameters:" height:50 width:maxWidth pos:[13,posY]
		spinner sailLightAbsorption "Light Absorption" range:[0,1,0] offset:[10,-35] fieldWidth:30 align:#left  tooltip:"Amount of light that don't go through the sail. (1 is full opaque, 0 let light passing through at 50%)"

		groupBox WindshieldParameters "Windshield parameters:" height:130 width:maxWidth pos:[13,posY + 110]
		spinner detail1Rough "Detail 1 (R) Rough:" range:[0,1,0.1] scale:1 fieldWidth:40 offset:[10, -115] align:#left across:2 tooltip:"Roughness of channel R of detail"
		spinner detail1Opacity "Detail 1 (R) Opacity:" range:[0,1,0.1] scale:1 fieldWidth:40 offset:[5, -115] align:#left tooltip:"Opacity of channel R of detail"
		spinner detail2Rough "Detail 2 (B) Rough:" range:[0,1,0.1] scale:1 fieldWidth:40 offset:[10, 0] align:#left across:2 tooltip:"Roughness of channel B of detail"
		spinner detail2Opacity "Detail 2 (B) Opacity:" range:[0,1,0.1] scale:1 fieldWidth:40 offset:[5, 0] align:#left tooltip:"Opacity of channel B of detail"
		spinner microScratchesTiling "Micro-Scratches Tiling:" range:[0,1000,1] scale:1 fieldWidth:40 offset:[10, 0] align:#left tooltip:"Tiling of micro-scratches"
		spinner microScratchesStrength "Micro-Scratches Strength:" range:[0,100,1] scale:1 fieldWidth:40 offset:[10, 0] align:#left tooltip:"Strength of micro-scratches"
		spinner detailNormalRefractScale "Detail Normal Refraction Strength:" range:[0,1,0.1] scale:1 fieldWidth:40 offset:[10, 0] align:#left across:2 tooltip:"Refraction Strength of the Detail Normal"

		groupBox WindshieldRainBox "Windshield Wipers parameters:" height:90 width:maxWidth pos:[13,posY + 250]
		checkbox wiperLines "Wiper Lines:" offset:[10,-77] across:3 align:#left tooltip:"Determine if they're wiper line due to wipers. Required WiperMask texture."
		spinner wiperLinesTiling "Tiling:"		range:[0,100,1] scale:1 fieldWidth:40 offset:[-34, -70] align:#right tooltip:"Tiling of wiper lines"
		spinner wiperLinesStrength "Strength:"	range:[0,10,1] scale:1 fieldWidth:40 offset:[-34, -70] align:#right tooltip:"Strength of wiper lines"
		groupBox WiperAnimStateBox "Wiper Animation:" height:40 width:(maxWidth-20) pos:[23,posY + 290]
		spinner wiperAnimState1 "Wiper1 State:" range:[0,1,0] scale:1 fieldWidth:40 offset:[20, -27] align:#left across:2 tooltip:"Wiper Animation State:"

		/*local PHPISideUIBoxScale = 0.7
		local PHPISpBaseValueScale = 0.01
		groupBox grpPHPI "Parallax Interior:" height:215 width:maxWidth pos:[13,posY]
		groupBox grpPHPIRoom "Room setup (meters):" height:65 width:(maxWidth*PHPISideUIBoxScale) offset:[7, -215+10]
		spinner spPHPIRoomSizeX "Size X:" range:[0,1000,2] scale:PHPISpBaseValueScale fieldWidth:40 offset:[-60, -50] align:#right tooltip:"(meters)\nHorizontal room size" across:2
		spinner spPHPIRoomOffsetX "Offset X:" range:[-10000,10000,0] scale:PHPISpBaseValueScale fieldWidth:45 offset:[-maxWidth*(1.0 - PHPISideUIBoxScale)-5, -50] align:#right tooltip:"(meters)\nHorizontal room offset"
		spinner spPHPIRoomSizeY "Size Y:" range:[0,1000,1] scale:PHPISpBaseValueScale fieldWidth:40 offset:[-60, 0] align:#right tooltip:"(meters)\nVertical room size" across:2
		spinner spPHPIRoomOffsetY "Offset Y:" range:[-10000,10000,0] scale:PHPISpBaseValueScale fieldWidth:45 offset:[-maxWidth*(1.0 - PHPISideUIBoxScale)-5, 0] align:#right tooltip:"(meters)\nVertical room offset"
		groupBox grpPHPIProjection "Seats setup:" height:65 width:(maxWidth*PHPISideUIBoxScale) offset:[7, 5]
		spinner spPHPIProjectionRatio "Ratio:" range:[0.001,1000.0,1] scale:(PHPISpBaseValueScale*0.1) fieldWidth:40 offset:[-60, -50] align:#right tooltip:"Side image width/height aspect ratio" across:2
		label lbPHPIProjectionRatio "<- side view Width/Height" offset:[-76, -50] enabled:false
		spinner spPHPIProjectionSize "Size %:" range:[1,1000,80] scale:(PHPISpBaseValueScale*0.1*100) fieldWidth:40 offset:[-60, 0] align:#right tooltip:"Seat size (% relative to room size)" across:2
		spinner spPHPIProjectionSpacingX "Spacing X %:" range:[0,100000,0] scale:(PHPISpBaseValueScale*0.1*100) fieldWidth:40 offset:[-maxWidth*(1.0 - PHPISideUIBoxScale)-5, 0] align:#right tooltip:"Spacing between seats (% relative to room size)"
		groupBox grpPHPISetup "Projection:" height:132 width:(maxWidth*(1.0 - PHPISideUIBoxScale)-18) pos:[25+maxWidth-(maxWidth*(1.0 - PHPISideUIBoxScale)),posY+15]
		checkbox chkPHPIUseSide "Side" checked:true enabled:false tooltip:"Use side projection" offset:[20+maxWidth-(maxWidth*(1.0 - PHPISideUIBoxScale)), -112]
		label lbPHPIUseSide "(mandatory)" enabled:false align:#left offset:[22+maxWidth-(maxWidth*(1.0 - PHPISideUIBoxScale)), -5]
		checkbox chkPHPIUseFront "Front" checked:false offset:[20+maxWidth-(maxWidth*(1.0 - PHPISideUIBoxScale)), 0] tooltip:"Use front projection"
		checkbox chkPHPIUseBack "Back" checked:false offset:[20+maxWidth-(maxWidth*(1.0 - PHPISideUIBoxScale)), 0] tooltip:"Use back projection"
		checkbox chkPHPIUseTop "Top" checked:false offset:[20+maxWidth-(maxWidth*(1.0 - PHPISideUIBoxScale)), 0] tooltip:"Use top projection"
		groupBox grpPHPIMisc "Misc:" height:60 width:(maxWidth-14) offset:[7, 15]
		checkbox chkPHPIMirrorLeftWall "Mirror left wall on right side" checked:true offset:[20, -60+13] tooltip:"Use only left wall texture and mirror on right side"
		spinner spPHPIRoomBackWallSizeOnTexture "Back wall: size on hallway texture %:" range:[0,100,50] scale:(PHPISpBaseValueScale * 100) fieldWidth:40 offset:[-20,0] align:#right \
			tooltip:"Space used by the back wall (the opposite wall facing view) on the hallway texture.\n(centered vertically)"*/
		
		-- Debug Shader Boxes
		groupBox DebugWindshieldBox "Debug Shader Windshield:" height:120 width:maxWidth pos:[13,posY + 350]
		checkbox debugWindshield_WiperMask "WiperMask" offset:[10,-107] align:#left tooltip:"..."
		checkbox debugWindshield_InsectsAlbedo "Insects Albedo:" offset:[10,0] align:#left tooltip:"..."
		spinner debugWindshield_InsectsMask "Insects Mask:" range:[0.0,1.0,1.0] scale:0.01 fieldWidth:50 offset:[10, 0] align:#left tooltip:"..."
		label debugWindshield_VertexColorLabel "Debug Vertex Color" offset:[10,0] align:#left
		radiobuttons debugWindshield_VertexColorRadio labels:#("off", "R", "G", "B", "A") offset:[10,0] align:#left columns:5 offsets:#([0,0], [12,0], [15,0], [20,0], [22,0])
		
		fn adjustUiHeight =
		(
			local decalBoxOffset =				if decalBox.visible				then decalBox.height			 + 10	else 0
			local tireBoxOffset =				if TireBox.visible				then TireBox.height				 + 10	else 0
			local clearcoatBoxOffset =			if clearcoatBox.visible			then clearcoatBox.height		 + 10	else 0
			local SSSboxOffset =				if SSSbox.visible				then SSSbox.height				 + 10	else 0
			local glassBoxOffset =				if GlassBox.visible				then GlassBox.height			 + 10	else 0
			local parallaxBoxOffset =			if ParallaxBox.visible			then ParallaxBox.height			 + 10	else 0
			local fresnelBoxOffset =			if fresnelBox.visible			then fresnelBox.height			 + 10	else 0
			local ghostBoxOffset =				if ghostBox.visible				then ghostBox.height			 + 10	else 0
			local pearlBoxOffset =				if pearlBox.visible				then pearlBox.height			 + 10	else 0
			local iridescentBoxOffset =			if iridescentBox.visible		then iridescentBox.height		 + 10	else 0
			local sailBoxOffset =				if sailBox.visible				then sailBox.height				 + 10	else 0
			local windshieldParametersOffset =	if WindshieldParameters.visible	then WindshieldParameters.height + 10	else 0
			local windshieldRainBoxOffset =		if WindshieldRainBox.visible	then WindshieldRainBox.height	 + 10	else 0
			local debugWindshieldBoxOffset =	if DebugWindshieldBox.visible	then DebugWindshieldBox.height	 + 10	else 0
			
			paramsUI.height = (posY \
				+ decalBoxOffset + tireBoxOffset + clearcoatBoxOffset + SSSboxOffset + glassBoxOffset + parallaxBoxOffset + fresnelBoxOffset \
				+ ghostBoxOffset + pearlBoxOffset + iridescentBoxOffset + sailBoxOffset + windshieldParametersOffset \
				+ windshieldRainBoxOffset + debugWindshieldBoxOffset) * uiScale \
				+ 10 -- + bottom margin
		)
		
		fn updateUI =
		(
			local paramsYoffset = 0
			occlusionStrength.text = "AO Strength"

			emissive.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			roughness.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			metallic.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder or matList[materialType.selection] == #Vegetation)
			occlusionStrength.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			normalScale.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			blendThreshold.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] ==#FresnelFade or matList[materialType.selection] == #EnvironmentOccluder or matList[materialType.selection] == #SSS)
			dirtUvScale.enabled = (matList[materialType.selection] == #Standard or matList[materialType.selection] ==#ClearCoat)
			dirtBlendSharpness.enabled = (matList[materialType.selection] == #Standard or matList[materialType.selection] ==#ClearCoat)
			dirtBlendAmount.enabled = (matList[materialType.selection] == #Standard or matList[materialType.selection] ==#ClearCoat)
			doubleSided.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			emissiveMul.enabled =  not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			dayNightCycle.enabled = (matList[materialType.selection] == #Standard or matList[materialType.selection] == #ClearCoat)
	
			UVParams.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			renderFlagBox.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			drawOrder.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)
			noCastShadow.enabled = not(matList[materialType.selection] == #Invisible or matList[materialType.selection] == #EnvironmentOccluder)

			alphaMode.enabled = alphaModeBox.enabled = (matList[materialType.selection] == #Standard or ( materialType.selection >= 9 and  materialType.selection <= 11) or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #ClearCoat)
			alphaCutoff.enabled = alphaMode.enabled and alphaMode.state == 2

			decalBox.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalBox.enabled = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			if(decalBox.enabled == true) then paramsYoffset += decalBox.height + 30
			decalColorFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalRoughnessFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalMetalFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalOcclusionFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalNormalFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalEmissiveFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalNormalOverrideFactor.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalBlendSharpnessFactor.visible = (matList[materialType.selection] == #GeoDecal_Dirt)
			decalRenderOnClearcoat.visible = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)
			decalRenderOnClearcoat.enabled = (matList[materialType.selection] == #Decal or matList[materialType.selection] == #GeoDecalFrosted or matList[materialType.selection] == #GeoDecal_Dirt)		

			SSSbox.visible = matList[materialType.selection] == #Hair
			SSSbox.enabled = matList[materialType.selection] == #Hair
			if(SSSbox.enabled == true) then paramsYoffset += SSSbox.height + 10
			SSSColor.visible = matList[materialType.selection] == #Hair 
			SSSColor.enabled = matList[materialType.selection] == #Hair

			TireBox.visible = (matList[materialType.selection] == #Tire)
			TireBox.enabled = (matList[materialType.selection] == #Tire)
			tireMudNormalTiling.visible = (matList[materialType.selection] == #Tire)
			tireMudNormalTiling.enabled = (matList[materialType.selection] == #Tire)
			tireMudAnimState.visible = (matList[materialType.selection] == #Tire)
			tireMudAnimState.enabled = (matList[materialType.selection] == #Tire)
			tireDustAnimState.visible = (matList[materialType.selection] == #Tire)
			tireDustAnimState.enabled = (matList[materialType.selection] == #Tire)

			GlassBox.visible = (matList[materialType.selection] == #Glass)
			GlassBox.enabled = (matList[materialType.selection] == #Glass)
			if(GlassBox.enabled == true) then paramsYoffset += GlassBox.height + 10
			glassWidthUI.visible = (matList[materialType.selection] == #Glass)
			glassWidthUI.enabled = (matList[materialType.selection] == #Glass)

			fresnelBox.visible = (matList[materialType.selection] == #FresnelFade)
			fresnelBox.enabled = (matList[materialType.selection] == #FresnelFade)
			if(fresnelBox.enabled == true) then paramsYoffset += fresnelBox.height + 10
			fresnelFactor.visible = (matList[materialType.selection] == #FresnelFade)
			fresnelFactor.enabled = (matList[materialType.selection] == #FresnelFade)
			fresnelOpacityOffset.visible = (matList[materialType.selection] == #FresnelFade)
			fresnelOpacityOffset.enabled = (matList[materialType.selection] == #FresnelFade)

			ghostBox.visible = (matList[materialType.selection] == #Ghost)
			ghostBox.enabled = (matList[materialType.selection] == #Ghost)
			if(ghostBox.enabled == true) then paramsYoffset += ghostBox.height + 10
			ghostPowerFactor.visible = (matList[materialType.selection] == #Ghost)
			ghostPowerFactor.enabled = (matList[materialType.selection] == #Ghost)
			ghostBiasFactor.visible = (matList[materialType.selection] == #Ghost)
			ghostBiasFactor.enabled = (matList[materialType.selection] == #Ghost)
			ghostScaleFactor.visible = (matList[materialType.selection] == #Ghost)
			ghostScaleFactor.enabled = (matList[materialType.selection] == #Ghost)

			pearlBox.visible = (matList[materialType.selection] == #Standard)
			pearlBox.enabled = (matList[materialType.selection] == #Standard)
			if(pearlBox.enabled == true) then paramsYoffset += pearlBox.height + 10
			pearlescent.visible = (matList[materialType.selection] == #Standard)
			pearlShift.visible = (matList[materialType.selection] == #Standard)
			pearlRange.visible = (matList[materialType.selection] == #Standard)
			pearlBrightness.visible = (matList[materialType.selection] == #Standard)
			pearlescent.enabled = (matList[materialType.selection] == #Standard)
			pearlShift.enabled = ((matList[materialType.selection] == #Standard) and pearlescent.checked == true)
			pearlRange.enabled = ((matList[materialType.selection] == #Standard) and pearlescent.checked == true)
			pearlBrightness.enabled = ((matList[materialType.selection] == #Standard) and pearlescent.checked == true)

			iridescentBox.visible = (matList[materialType.selection] == #Windshield)
			iridescentBox.enabled = (matList[materialType.selection] == #Windshield)
			if(iridescentBox.enabled == true) then paramsYoffset += iridescentBox.height + 10
			iridescent.visible = (matList[materialType.selection] == #Windshield)
			iridescentMinThickness.visible = (matList[materialType.selection] == #Windshield)
			iridescentMaxThickness.visible = (matList[materialType.selection] == #Windshield)
			iridescentBrightness.visible = (matList[materialType.selection] == #Windshield)
			iridescent.enabled = (matList[materialType.selection] == #Windshield)
			iridescentMinThickness.enabled = ((matList[materialType.selection] == #Windshield) and iridescent.checked == true)
			iridescentMaxThickness.enabled = ((matList[materialType.selection] == #Windshield) and iridescent.checked == true)
			iridescentBrightness.enabled = ((matList[materialType.selection] == #Windshield) and iridescent.checked == true)

			sailBox.visible = matList[materialType.selection] == #Sail
			sailBox.enabled = matList[materialType.selection] == #Sail
			if(sailBox.enabled == true) then paramsYoffset += sailBox.height + 10
			sailLightAbsorption.visible = matList[materialType.selection] == #Sail
			sailLightAbsorption.enabled = matList[materialType.selection] == #Sail

			clearcoatBox.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatBox.enabled = (matList[materialType.selection] == #ClearCoat)
			if(clearcoatBox.enabled == true) then paramsYoffset += clearcoatBox.height + 10
			clearcoatRoughnessFactor.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatRoughnessFactor.enabled = (matList[materialType.selection] == #ClearCoat)
			clearcoatNormalFactor.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatNormalFactor.enabled = (matList[materialType.selection] == #ClearCoat)
			clearcoatColorRoughnessTiling.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatColorRoughnessTiling.enabled = (matList[materialType.selection] == #ClearCoat)
			clearcoatNormalTiling.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatNormalTiling.enabled = (matList[materialType.selection] == #ClearCoat)
			clearcoatInverseRoughness.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatInverseRoughness.enabled = (matList[materialType.selection] == #ClearCoat)
			clearcoatBaseRoughness.visible = (matList[materialType.selection] == #ClearCoat)
			clearcoatBaseRoughness.enabled = (matList[materialType.selection] == #ClearCoat and clearcoatInverseRoughness.checked == true)

			--if parallax, we don't have a detail map.
			detailUVScale.enabled = not(matList[materialType.selection] == #ParallaxWindow or matList[materialType.selection] == #Invisible or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #EnvironmentOccluder or matList[materialType.selection] == #SSS)
			detailNormalScale.enabled = not(matList[materialType.selection] == #ParallaxWindow or matList[materialType.selection] == #Invisible or matList[materialType.selection] == #FresnelFade or matList[materialType.selection] == #EnvironmentOccluder or matList[materialType.selection] == #SSS)
			ParallaxBox.visible = (matList[materialType.selection] == #ParallaxWindow)
			parallaxScale.visible = (matList[materialType.selection] == #ParallaxWindow)
			parallaxScale.enabled = (matList[materialType.selection] == #ParallaxWindow)
			roomSizeXScale.visible =  (matList[materialType.selection] == #ParallaxWindow)
			roomSizeXScale.enabled =  (matList[materialType.selection] == #ParallaxWindow)
			roomSizeYScale.visible =  (matList[materialType.selection] == #ParallaxWindow)
			roomSizeYScale.enabled =  (matList[materialType.selection] == #ParallaxWindow)
			roomNumberXY.visible =  (matList[materialType.selection] == #ParallaxWindow)
			roomNumberXY.enabled =  (matList[materialType.selection] == #ParallaxWindow)
			corridor.visible =  (matList[materialType.selection] == #ParallaxWindow)
			corridor.enabled = (matList[materialType.selection] == #ParallaxWindow)
			if(ParallaxBox.visible == true) then paramsYoffset += ParallaxBox.height + 10
			
			clampUVX.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			clampUVY.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			UVOffsetU.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			UVOffsetV.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			UVTilingU.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			UVTilingV.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			UVRotation.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)

			gameplayBox.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)

			rainBox.enabled = (matList[materialType.selection] == #ClearCoat or matList[materialType.selection] == #Windshield)
			canReceiveRain.enabled = (matList[materialType.selection] == #ClearCoat or matList[materialType.selection] == #Windshield)
			rainDropScale.enabled = (matList[materialType.selection] == #ClearCoat or matList[materialType.selection] == #Windshield) and canReceiveRain.checked == true

			collisionMaterial.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			roadMaterial.enabled = not(matList[materialType.selection] == #EnvironmentOccluder)
			disableMotionBlur.enabled = not(matList[materialType.selection] == #EnvironmentOccluder or matList[materialType.selection] == #Invisible)
			flipBackFace.enabled = not(matList[materialType.selection] == #EnvironmentOccluder or matList[materialType.selection] == #Sail or doubleSided.checked == false)

			WindshieldParameters.enabled = matList[materialType.selection] == #Windshield
			WindshieldParameters.visible = matList[materialType.selection] == #Windshield
			if(WindshieldParameters.enabled == true) then paramsYoffset += WindshieldParameters.height + 10
			detail1Rough.enabled = matList[materialType.selection] == #Windshield
			detail1Rough.visible = matList[materialType.selection] == #Windshield
			detail2Rough.enabled = matList[materialType.selection] == #Windshield
			detail2Rough.visible = matList[materialType.selection] == #Windshield
			detail1Opacity.enabled = matList[materialType.selection] == #Windshield
			detail1Opacity.visible = matList[materialType.selection] == #Windshield
			detail2Opacity.enabled = matList[materialType.selection] == #Windshield
			detail2Opacity.visible = matList[materialType.selection] == #Windshield
			microScratchesTiling.enabled = matList[materialType.selection] == #Windshield
			microScratchesTiling.visible = matList[materialType.selection] == #Windshield
			microScratchesStrength.enabled = matList[materialType.selection] == #Windshield
			microScratchesStrength.visible = matList[materialType.selection] == #Windshield
			detailNormalRefractScale.enabled = matList[materialType.selection] == #Windshield
			detailNormalRefractScale.visible = matList[materialType.selection] == #Windshield

			reflectionMaskLabel.visible = matList[materialType.selection] == #Windshield
			if (matList[materialType.selection] == #Windshield) then
			(
				occlusionStrength.text = ""
			)

			WindshieldRainBox.visible = matList[materialType.selection] == #Windshield
			WindshieldRainBox.enabled = matList[materialType.selection] == #Windshield
			if(WindshieldRainBox.enabled == true) then paramsYoffset += WindshieldRainBox.height + 10
			-- rainDropSide.visible = matList[materialType.selection] == #Windshield
			wiperLines.visible = matList[materialType.selection] == #Windshield
			wiperLinesTiling.visible = matList[materialType.selection] == #Windshield
			wiperLinesStrength.visible = matList[materialType.selection] == #Windshield
			wiperAnimStateBox.visible = matList[materialType.selection] == #Windshield
			wiperAnimState1.visible = matList[materialType.selection] == #Windshield

			WindshieldRainBox.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true
			rainDropSide.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true
			wiperLines.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true
			wiperLinesTiling.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true and wiperLines.checked == true
			wiperLinesStrength.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true and wiperLines.checked == true
			wiperAnimStateBox.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true
			if(wiperAnimStateBox.enabled == true) then paramsYoffset += wiperAnimStateBox.height + 10
			wiperAnimState1.enabled = matList[materialType.selection] == #Windshield and canReceiveRain.checked == true
			
			DebugWindshieldBox.visible = matList[materialType.selection] == #Windshield
			DebugWindshieldBox.enabled = matList[materialType.selection] == #Windshield
			if(DebugWindshieldBox.enabled == true) then paramsYoffset += DebugWindshieldBox.height + 10
			debugWindshield_WiperMask.visible = matList[materialType.selection] == #Windshield
			debugWindshield_InsectsAlbedo.visible = matList[materialType.selection] == #Windshield
			debugWindshield_InsectsMask.visible = matList[materialType.selection] == #Windshield
			debugWindshield_InsectsMask.enabled = debugWindshield_InsectsAlbedo.checked == true
			debugWindshield_VertexColorLabel.visible = matList[materialType.selection] == #Windshield

			/*grpPHPI.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			grpPHPIRoom.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIRoomSizeX.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIRoomOffsetX.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIRoomSizeY.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIRoomOffsetY.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			grpPHPIProjection.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIProjectionRatio.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			lbPHPIProjectionRatio.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIProjectionSize.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIProjectionSpacingX.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			grpPHPISetup.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			chkPHPIUseSide.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			lbPHPIUseSide.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			chkPHPIUseFront.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			chkPHPIUseBack.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			chkPHPIUseTop.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			grpPHPIMisc.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			chkPHPIMirrorLeftWall.visible = matList[materialType.selection] == #PortHoleParallaxInterior
			spPHPIRoomBackWallSizeOnTexture.visible = matList[materialType.selection] == #PortHoleParallaxInterior*/

			if (matList[materialType.selection] == #GeoDecalFrosted) then
			(
				decalEmissiveFactor.text = "Melt Sys:"
				decalOcclusionFactor.text = "Blast Sys:"
			)
			else
			(
				decalEmissiveFactor.text = "Emissive:"
				decalOcclusionFactor.text = "Occlusion:"
			)
			if (matList[materialType.selection] == #Windshield) then
			(
				metallic.value = 0
				debugWindshield_VertexColorRadio.state = 1
			)
			if (matList[materialType.selection] == #Glass) then
			(
				metallic.value = 0
			)
			if (matList[materialType.selection] == #Vegetation) then
			(
				metallic.value = 1
			)
			if (matList[materialType.selection] == #ParallaxWindow) then
			(
				alphaMode.state = 1
			)
			if(matList[materialType.selection] == #Ghost) then 
			(
				noCastShadow.enabled = false
				noCastShadow.checked = true
				alphaMode.state = 3
			)
			if(matList[materialType.selection] == #Propeller) then 
			(
				alphaMode.state = 1
			)
			if(matList[materialType.selection] == #GeoDecalFrosted) then 
			(
				delegate.p_decalFrosted = true
				alphaMode.state = 3
			)
			/*if (matList[materialType.selection] == #PortholeParallaxInterior) then
			(
				-- Setup defaults
				metallic.value = 0
				roughness.value = 0.3
				emissive.color = color 255 255 255
			)*/
			
			adjustUiHeight()
		)

		on materialType selected val do
		(
			if (matList[materialType.selection] == #NotUsed1) then
				materialType.selection = 1 -- set to default material when select a notUsed material

			updateGlobalUI()
			loadShader()
			completeRedraw()
		)

		on pearlescent changed val do 
		(
			loadShader()
			completeRedraw()
			updateUI()
		)

		on iridescent changed val do 
		(
			loadShader()
			completeRedraw()
			updateUI()
			updateGlobalUI()
		)
		
		on canReceiveRain changed val do
		(
			updateUI()
		)

		on clearcoatInverseRoughness changed val do
		(
			updateGlobalUI()
		)

		on wiperLines changed val do
		(
			updateUI()
		)

		on alphaMode changed val do
		(
			updateUI()
		)
		
		on glassWidthUI changed val do 
		(
			this.glassWidth = val / 1000.0
		)

		on doubleSided changed val do
		(
			updateUI()
		)

		on debugWindshield_InsectsAlbedo changed val do (updateUI())

		on paramsUI open do
		(
			paramsUI.open = MSFS2024_paramsRolledUp
			updateUI()
			glassWidthUI.value = this.glassWidth * 1000.0
		)

		on paramsUI rolledUp state do
		(
			MSFS2024_paramsRolledUp = state
		)

		on chart pressed do filein "MSFS2024_Chart.ms"

		on emissionCalc pressed do filein "MSFS2024_EmissionCalc.ms"
	)

	rollout texturesUI "Textures"
	(
		local uiScale = MSFS2024_getUiScale()
		
		local maxWidth = (texturesUI.width - 30)
		
		local texSlotHeights = #(20, 32, 80)
		local texBtnSize = [maxwidth, texSlotHeights[texSlotHeights.count]] --init with largest so we always will have enough space
		local texBtnFirstYOffset = 30
		local texBtnDefaultExtraYSeparation = 5
		
		checkbutton chkbtnQuickPreview "Quick preview" tooltip:"Quick texture preview\n\nMay not work properly if multiple monitors and DPI scalings" \
			iconName:@"RenderFrameWindow\ToggleUI" iconSize:[16, 16] align:#left offset:[0, -5] across:3
		label lbTexSlotSize "Display size:" align:#left offset:[-80, 0]
		radiobuttons texSlotSize "" labels:#("small", "medium", "large") tooltip:"change texture slot display below" default:2 columns:3 align:#left offset:[-126,0] offsets:#([0,0], [-5,0], [0,0])
		--button btnClearAllSlots "Clear" tooltip:"Clear all texture slots" align:#right offset:[106,-23] across:2
		--button btnReloadUI "Reload" tooltip:"Reload texture slots" align:#right offset:[-5,-23]
		button btnReloadUI "Reload" tooltip:"Reload all texture slots" iconName:@"Common\RotateCW" iconSize:[16, 16] width:40 align:#right offset:[130,-27] across:2
		button btnClearAllSlots "Clear" tooltip:"Clear all texture slots" iconName:@"CommandPanel\Motion\BipedRollout\CopyAndPaste\DeleteCollection" iconSize:[16, 16] align:#right offset:[-5, -27]
		
		dotnetcontrol BaseColorTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnFirstYOffset]
		dotnetcontrol OcclusionRoughnessMetallicTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol NormalTexBtn								"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol EmissiveTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol DetailColorTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol DetailOcclusionRoughnessMetallicTexBtn	"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol DetailNormalTexBtn						"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol BlendMaskTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol FoliageMaskTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol OcclusionTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol AnisoDirectionRoughnessTexBtn				"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol WetnessAOTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol WiperMaskTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol WindshieldDetailNormalTexBtn				"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol ScratchesNormalTexBtn						"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol ClearcoatColorRoughnessTexBtn				"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol ClearcoatNormalTexBtn						"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol DirtTexBtn								"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol OpacityTexBtn								"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol IridescentThicknessTexBtn					"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol WindshieldInsectsTexBtn					"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol WindshieldInsectsMaskTexBtn				"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol DirtOcclusionRoughnessMetallicTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol TireDetailsTexBtn							"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol TireMudNormalTexBtn						"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		
		-- Porthole parallax Interior
		/*dotnetcontrol PHPIInteriorHallwayAlbedoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPIInteriorHallwayNormalAoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIInteriorHallwayEmissiveTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIInteriorLeftWallAlbedoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPIInteriorLeftWallNormalAoTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIInteriorLeftWallEmissiveTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIInteriorRightWallAlbedoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPIInteriorRightWallNormalAoTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIInteriorRightWallEmissiveTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPISideProjectionAlbedoHeightTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPISideProjectionNormalAoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPISideProjectionEmissiveTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIFrontProjectionAlbedoHeightTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPIFrontProjectionNormalAoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIFrontProjectionEmissiveTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIBackProjectionAlbedoHeightTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPIBackProjectionNormalAoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPIBackProjectionEmissiveTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPITopProjectionAlbedoHeightTexBtn		"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y offset:[0,texBtnDefaultExtraYSeparation]
		dotnetcontrol PHPITopProjectionNormalAoTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y
		dotnetcontrol PHPITopProjectionEmissiveTexBtn			"system.windows.forms.button" width:texBtnSize.x height:texBtnSize.y*/



		-- variable contenant le nom de la texture ciblee lors du clic droit
		local activeTex
		
		local texBtns = #(
			BaseColorTexBtn,
			OcclusionRoughnessMetallicTexBtn,
			NormalTexBtn,
			EmissiveTexBtn,
			DetailColorTexBtn,
			DetailOcclusionRoughnessMetallicTexBtn,
			DetailNormalTexBtn,
			BlendMaskTexBtn,
			FoliageMaskTexBtn,
			OcclusionTexBtn,
			AnisoDirectionRoughnessTexBtn,
			WetnessAOTexBtn,
			WiperMaskTexBtn,
			WindshieldDetailNormalTexBtn,
			ScratchesNormalTexBtn,
			ClearcoatColorRoughnessTexBtn,
			ClearcoatNormalTexBtn,
			DirtTexBtn,
			OpacityTexBtn,
			IridescentThicknessTexBtn,
			WindshieldInsectsTexBtn,
			WindshieldInsectsMaskTexBtn,
			DirtOcclusionRoughnessMetallicTexBtn,
			TireDetailsTexBtn,
			TireMudNormalTexBtn
			-- Porthole parallax Interior
			/*PHPIInteriorHallwayAlbedoTexBtn,
			PHPIInteriorHallwayNormalAoTexBtn,
			PHPIInteriorHallwayEmissiveTexBtn,
			PHPIInteriorLeftWallAlbedoTexBtn,
			PHPIInteriorLeftWallNormalAoTexBtn,
			PHPIInteriorLeftWallEmissiveTexBtn,
			PHPIInteriorRightWallAlbedoTexBtn,
			PHPIInteriorRightWallNormalAoTexBtn,
			PHPIInteriorRightWallEmissiveTexBtn,
			PHPISideProjectionAlbedoHeightTexBtn,
			PHPISideProjectionNormalAoTexBtn,
			PHPISideProjectionEmissiveTexBtn,
			PHPIFrontProjectionAlbedoHeightTexBtn,
			PHPIFrontProjectionNormalAoTexBtn,
			PHPIFrontProjectionEmissiveTexBtn,
			PHPIBackProjectionAlbedoHeightTexBtn,
			PHPIBackProjectionNormalAoTexBtn,
			PHPIBackProjectionEmissiveTexBtn,
			PHPITopProjectionAlbedoHeightTexBtn,
			PHPITopProjectionNormalAoTexBtn,
			PHPITopProjectionEmissiveTexBtn*/
		)
		local texBtnsPos --filled on rollout open handler
		local texBtnsErrorState --filled on rollout open handler
		-- buttons appearance
		local btnStyle = (dotNetClass "System.Windows.Forms.FlatStyle").flat -- Flat / Popup / Standard / System
		local btnColor = (dotnetclass "system.drawing.color").FromArgb 102 102 102
		local btnHoverColor = (dotnetclass "system.drawing.color").FromArgb 121 121 121
		local btnErrorColor = (dotnetclass "system.drawing.color").FromArgb 179 51 51
		local btnBorderColor = (dotnetclass "system.drawing.color").FromArgb 68 68 68
		local btnHoverBorderColor = (dotnetclass "system.drawing.color").FromArgb 153 153 153
		local btnErrorBorderColor = (dotnetclass "system.drawing.color").FromArgb 255 0 0
		local btnBorderSize = 1
		local btnErrorHoverBorderSize = 2
		local btnMargin = dotNetObject "System.Windows.Forms.Padding" 0 0 0 0
		local btnPadding = dotNetObject "System.Windows.Forms.Padding" 0 0 0 0
		local btnHoverForeColor = (dotnetclass "system.drawing.color").FromArgb 13 13 13
		local btnForeColor = (dotnetclass "system.drawing.color").FromArgb 228 228 228
		local btnFont = dotNetObject "System.Drawing.Font" "Arial" (11 * uiScale) (dotNetClass "System.Drawing.GraphicsUnit").Pixel --(dotNetClass "System.Drawing.FontStyle").bold
		local btnTooltip = dotnetobject "System.Windows.Forms.ToolTip"
		fn getSlotErrorState slot =
		(
			local thisID = findItem texBtns slot
			thisID != 0 and texBtnsErrorState[thisID]
		)
		fn setSlotHoverState slot basename =
		(
			if getSlotErrorState slot then --handle error state
			(
				slot.FlatAppearance.BorderColor = btnErrorBorderColor
				slot.FlatAppearance.BorderSize = btnErrorHoverBorderSize
			)
			else
			(
				slot.FlatAppearance.BorderColor = btnHoverBorderColor
				slot.FlatAppearance.BorderSize = btnBorderSize
			)
			slot.backColor = btnHoverColor
			slot.ForeColor = btnHoverForeColor
			
			MSFS2024_displayTexturePreview slot basename
		)
		fn setSlotBaseState slot =
		(
			if getSlotErrorState slot then --handle error state
			(
				slot.backColor = btnErrorColor
				slot.FlatAppearance.BorderColor = btnErrorBorderColor
			)
			else
			(
				slot.backColor = btnColor
				slot.FlatAppearance.BorderColor = btnBorderColor
			)
			slot.FlatAppearance.BorderSize = btnBorderSize
			slot.ForeColor = btnForeColor
			
			MSFS2024_hideTexturePreview()
		)
		fn initTextureSlots =
		(
-- 			btnTooltip.ShowAlways = true -- display even with texture preview window
			texBtnSize.y = texSlotHeights[texSlotSize.state]
			for slot in texBtns do
			(
				slot.height = texBtnSize.y
				slot.TextAlign = slot.TextAlign.MiddleCenter --TopLeft
				slot.BackgroundImageLayout = slot.BackgroundImageLayout.Zoom --Center, None, Stretch, Tile, Zoom
				slot.AllowDrop = true
				slot.FlatStyle = btnStyle
				slot.FlatAppearance.BorderSize = btnBorderSize
				slot.Margin = btnMargin
				slot.Padding = btnPadding
				
				setSlotBaseState slot
			)
		)
		fn adjustTexSlotsSize =
		(
			for slot in texBtns do slot.height = texBtnSize.y
		)
		fn adjustTexSlotsPositionAndRolloutHeight =
		(
			local yAdd = texBtnSize.y
			local yOffset = 0
			for i=1 to texBtns.count do
			(
				if texBtns[i].visible then
				(
					yOffset += (if i > 1 then texBtnsPos[i].y - texBtnSize.y - (texSlotHeights[texSlotHeights.count] - texSlotHeights[texSlotSize.state]) - texBtnsPos[i-1].y else texBtnFirstYOffset) -- keep original separation above texture slot -> allow custom spacing
					texBtns[i].pos = [texBtnsPos[i].x, yOffset]
					yOffset += yAdd				)
			)
			this.texturesUI.height = (if yOffset == 0 then texBtnFirstYOffset else yOffset * uiScale) + 30 -- + bottom margin
		)
		fn setTextureSlotText slot txt: =
		(
			slot.text = if txt != unsupplied then txt else "Texture"
			slot.font = btnFont -- for some reason updating dotnet controls reset font -> lets re-assign it
		)
		fn activateTextureSlot slot txt: =
		(
			slot.visible = true
			setTextureSlotText slot txt:txt
			slot.enabled = true
		)
		fn deactivateTextureSlot slot =
		(
			slot.visible = false
			slot.pos = [-maxWidth, 0] --"remove" annoying buttons filling the space even if invisible
			setTextureSlotText slot txt:"disabled"
			slot.enabled = false
		)
		-- disable all texture slots
		fn disableAllTextureSlots =
		(
			for o in texBtns do deactivateTextureSlot o
		)
		fn useDefaultTextureSlots =
		(
			activateTextureSlot BaseColorTexBtn							txt:"Base Color"
			activateTextureSlot OcclusionRoughnessMetallicTexBtn		txt:"Occlusion (R), Roughness (G), Metallic (B)"
			activateTextureSlot NormalTexBtn							txt:"Normal"
			activateTextureSlot EmissiveTexBtn							txt:"Emissive"
			
			activateTextureSlot BlendMaskTexBtn							txt:"Blend Mask"

			if(BlendMaskTex == "") then
			(
				activateTextureSlot DetailColorTexBtn						txt:"Detail Color (RGB), Alpha (A)"
				activateTextureSlot DetailNormalTexBtn						txt:"Detail Normal"
				activateTextureSlot DetailOcclusionRoughnessMetallicTexBtn	txt:"Detail Occlusion (R), Roughness (G), Metallic (B)"
				delegate.p_blendmaskEnabled = false
				this.paramsUI.blendThreshold.enabled = false
			)
			else
			(
				activateTextureSlot DetailColorTexBtn						txt:"Secondary Color (RGB), Alpha (A)"
				activateTextureSlot DetailNormalTexBtn						txt:"Secondary Normal"
				activateTextureSlot DetailOcclusionRoughnessMetallicTexBtn	txt:"Secondary Occ (R), Rough (G), Metal (B)"
				delegate.p_blendmaskEnabled = true
				this.paramsUI.blendThreshold.enabled = true
			)
			activateTextureSlot OcclusionTexBtn								txt:"Occlusion (UV2)"
			activateTextureSlot DirtTexBtn									txt:"Wear Albedo (RGB), Mask (A)"
			activateTextureSlot DirtOcclusionRoughnessMetallicTexBtn		txt:"Wear Occlusion(R), Roughness(G), Metallic(B), Intensity(A)"
		)
		-- texture slots update
		fn updateTexSlots =
		(
			adjustTexSlotsSize()
			disableAllTextureSlots() -- start by disabling everything

			case matList[this.materialType] of
			(
				#Decal: --GeoDecal
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#Windshield: --WindShield
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					setTextureSlotText EmissiveTexBtn							txt:"Secondary Details (RGBA)"
					activateTextureSlot WiperMaskTexBtn							txt:"Wiper Mask (RGBA)"
					activateTextureSlot WindshieldDetailNormalTexBtn			txt:"Detail Normal (use Detail UV Tiling)"
					setTextureSlotText DetailColorTexBtn						txt:"Details 1 (R), Icing Mask (G), Details 2 (B)"
					setTextureSlotText DetailNormalTexBtn						txt:"Icing Normal (use Detail UV Tiling)"
					setTextureSlotText OcclusionRoughnessMetallicTexBtn			txt:"Reflection (R), Roughness (G), Metallic (B)"
					setTextureSlotText DetailOcclusionRoughnessMetallicTexBtn	txt:"Detail Reflection (R), Detail Roughness(G), Detail Metallic (B)"
					setTextureSlotText OcclusionTexBtn							txt:"Reflection Mask (UV2)"
					activateTextureSlot ScratchesNormalTexBtn					txt:"Scratches Normal"
					activateTextureSlot WindshieldInsectsTexBtn					txt:"Insects Albedo (RGBA)"
					activateTextureSlot WindshieldInsectsMaskTexBtn				txt:"Insects Mask (A)"

					if ((getProperty this.paramsUI ("iridescent")).checked == true) then
					(
						activateTextureSlot IridescentThicknessTexBtn			txt:"Iridescent Thickness (R)"
					)
					else
					(
						deactivateTextureSlot IridescentThicknessTexBtn
					)

					deactivateTextureSlot BlendMaskTexBtn

					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#GeoDecalFrosted: --GeoDecalFrosted
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					deactivateTextureSlot BlendMaskTexBtn
					setTextureSlotText DetailOcclusionRoughnessMetallicTexBtn	txt:"Melt pattern (R), Roughness (G), Metallic (B)"
					delegate.p_blendmaskEnabled = false
					delegate.p_decalFrosted = true
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#GeoDecal_Dirt:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					activateTextureSlot BlendMaskTexBtn							txt:"GeometryDecal Blend Mask"
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#ClearCoat:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					if ((getProperty this.paramsUI ("clearcoatInverseRoughness")).checked == false) then
					(
						activateTextureSlot ClearcoatColorRoughnessTexBtn			txt:"Clearcoat Color (RGB), Clearcoat Roughness (A)"
						setTextureSlotText OcclusionRoughnessMetallicTexBtn			txt:"Occlusion (R), Clearcoat Roughness (G), Metallic (B)"
					)
					else
					(
						setTextureSlotText ClearcoatColorRoughnessTexBtn			txt:"disabled in clearcoat parameters"
					)
					activateTextureSlot ClearcoatNormalTexBtn						txt:"Clearcoat Normal"
				)
				#ParallaxWindow:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					setTextureSlotText BaseColorTexBtn							txt:"Front Glass Color"
					setTextureSlotText OcclusionRoughnessMetallicTexBtn			txt:"Occlusion (R), Roughness (G), Metallic (B)"
					setTextureSlotText NormalTexBtn								txt:"Front Glass Normal"
					activateTextureSlot DetailColorTexBtn						txt:"Behind Glass Color (RGB), Alpha (A)"
					activateTextureSlot EmissiveTexBtn							txt:"Emissive Ins Window (RGB), offset Time (A)"
					deactivateTextureSlot DetailNormalTexBtn
					deactivateTextureSlot DetailOcclusionRoughnessMetallicTexBtn
					deactivateTextureSlot BlendMaskTexBtn
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#Anisotropic:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					setTextureSlotText OcclusionRoughnessMetallicTexBtn			txt:"Occlusion (R), Aniso RoughnessX (G), Metallic (B)"
					activateTextureSlot AnisoDirectionRoughnessTexBtn			txt:"Aniso Direction (RG), RoughnessY (B)"
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#Hair:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					setTextureSlotText OcclusionRoughnessMetallicTexBtn			txt:"Occlusion (R), Aniso RoughnessX (G), Metallic (B)"
					activateTextureSlot AnisoDirectionRoughnessTexBtn			txt:"Aniso Direction (RG), RoughnessY (B)"
					deactivateTextureSlot DetailColorTexBtn
					deactivateTextureSlot DetailNormalTexBtn
					deactivateTextureSlot DetailOcclusionRoughnessMetallicTexBtn
					deactivateTextureSlot BlendMaskTexBtn
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#SSS:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					deactivateTextureSlot DetailColorTexBtn
					deactivateTextureSlot DetailNormalTexBtn
					deactivateTextureSlot DetailOcclusionRoughnessMetallicTexBtn
					deactivateTextureSlot BlendMaskTexBtn
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn

					activateTextureSlot OpacityTexBtn							txt:"Opacity"
				)
				#Invisible:
				(
					-- nothing
				)
				#FresnelFade:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not
					
					deactivateTextureSlot BlendMaskTexBtn
					deactivateTextureSlot DetailColorTexBtn
					deactivateTextureSlot DetailNormalTexBtn
					deactivateTextureSlot DetailOcclusionRoughnessMetallicTexBtn
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)
				#Ghost:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					delegate.p_blendmaskEnabled = false
					deactivateTextureSlot DirtTexBtn
					deactivateTextureSlot DirtOcclusionRoughnessMetallicTexBtn
				)				
				#EnvironmentOccluder:
				(
					-- nothing
				)
				#Tree:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					activateTextureSlot FoliageMaskTexBtn						txt:"Foliage Mask (R), Translucency (G), WindMask (B)"
				)
				#Vegetation:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not

					activateTextureSlot FoliageMaskTexBtn						txt:"Foliage Mask (R), Translucency (G), WindMask (B)"
				)
				#Tire:
				(
					useDefaultTextureSlots() --is this necessary ? -> remove comment if it is, remove line if not
					
					activateTextureSlot TireDetailsTexBtn						txt:"Tire Details : Mud (R), Dust (G)"
					activateTextureSlot TireMudNormalTexBtn						txt:"Tire Mud Normal"
					activateTextureSlot BlendMaskTexBtn							txt:"Tire Mud Cutout"
				)
				/*#PortholeParallaxInterior:
				(
					activateTextureSlot BaseColorTexBtn							txt:"Porthole Albedo (RGB), Depth (A)"
					activateTextureSlot OcclusionRoughnessMetallicTexBtn		txt:"Porthole AO (R), Roughness (G), Metallic (B)"
					activateTextureSlot NormalTexBtn							txt:"Porthole normal (RGB)"

					activateTextureSlot PHPIInteriorHallwayAlbedoTexBtn			txt:"Interior hallway Albedo (RGBA)"
					activateTextureSlot PHPIInteriorHallwayNormalAoTexBtn		txt:"Interior hallway Normal (RGB), AO (A)"
					activateTextureSlot PHPIInteriorHallwayEmissiveTexBtn		txt:"Interior hallway Emissive (RGB)"
					activateTextureSlot PHPIInteriorLeftWallAlbedoTexBtn		txt:"Interior left wall Albedo (RGBA)"	
					activateTextureSlot PHPIInteriorLeftWallNormalAoTexBtn		txt:"Interior left wall Normal (RGB), AO (A)"
					activateTextureSlot PHPIInteriorLeftWallEmissiveTexBtn		txt:"Interior left wall Emissive (RGB)"
					if not PHPIMirrorLeftWall then
					(
						activateTextureSlot PHPIInteriorRightWallAlbedoTexBtn		txt:"Interior right wall Albedo (RGBA)"	
						activateTextureSlot PHPIInteriorRightWallNormalAoTexBtn		txt:"Interior right wall Normal (RGB), AO (A)"
						activateTextureSlot PHPIInteriorRightWallEmissiveTexBtn		txt:"Interior right wall Emissive (RGB)"
					)
					activateTextureSlot PHPISideProjectionAlbedoHeightTexBtn	txt:"Side projection Albedo (RGB), Height (A)"
					activateTextureSlot PHPISideProjectionNormalAoTexBtn		txt:"Side projection Normal (RGB), AO (A)"
					activateTextureSlot PHPISideProjectionEmissiveTexBtn		txt:"Side projection Emissive (RGB)"
					if this.PHPIUseFront then
					(
						activateTextureSlot PHPIFrontProjectionAlbedoHeightTexBtn	txt:"Front projection Albedo (RGB), Height (A)"
						activateTextureSlot PHPIFrontProjectionNormalAoTexBtn		txt:"Front projection Normal (RGB), AO (A)"
						activateTextureSlot PHPIFrontProjectionEmissiveTexBtn		txt:"Front projection Emissive (RGB)"
					)
					if this.PHPIUseBack then
					(
						activateTextureSlot PHPIBackProjectionAlbedoHeightTexBtn	txt:"Back projection Albedo (RGB), Height (A)"
						activateTextureSlot PHPIBackProjectionNormalAoTexBtn		txt:"Back projection Normal (RGB), AO (A)"
						activateTextureSlot PHPIBackProjectionEmissiveTexBtn		txt:"Back projection Emissive (RGB)"
					)
					if this.PHPIUseTop then
					(
						activateTextureSlot PHPITopProjectionAlbedoHeightTexBtn		txt:"Top projection Albedo (RGB), Height (A)"
						activateTextureSlot PHPITopProjectionNormalAoTexBtn			txt:"Top projection Normal (RGB), AO (A)"
						activateTextureSlot PHPITopProjectionEmissiveTexBtn			txt:"Top projection Emissive (RGB)"
					)
				)*/
				default:
				(
					useDefaultTextureSlots()
				)
			)

			adjustTexSlotsPositionAndRolloutHeight()
		)

		-- function update the display of texture (UI only) and tooltip
		fn updateUiBm basename =
		(
			local filename = getProperty this (basename + "Tex")
			local btn = getProperty this.texturesUI (basename + "TexBtn")
			local thisID = findItem texBtns btn
			if filename != "" and filename != undefined then
			(
				if getFullFilePath &filename then -- TODO: seems to fail systematically with relative path (tested with texture in project root folder)
				(
					-- Image
					local tex
					try( tex	= getProperty delegate (getDelTexPName basename) )
					catch( tex = undefined )
					if tex == undefined then tex = openBitMap filename
					if (tex != undefined) then
					(
-- 						if MSFS2024_isTexturePreviewActive() then
-- 						(
-- 							btnTooltip.SetToolTip btn ""
-- 						)
-- 						else
						(
							-- TFlags
							local TFlagsFile = getFilenamePath filename + (filenameFromPath filename) + ".FLAGS"
							local TFlags = ""
							local stream = openFile TFlagsFile
							if stream != undefined then
							(
								TFlags = "TFlags:\n"
								TFlags += readDelimitedString stream #eof
								close stream
							)
							
							-- Tooltip
							local bminfo = getBitmapInfo tex
							
							local txt = btn.text + "\n" \
								+ filename + "\n" \
								+ bminfo[3] as string + "*"+ bminfo[4] as string + " Alpha:" + bminfo[9] as string + " Bits:" + bminfo[5] as string + "\n" \
								+ TFlags
							
							btnTooltip.SetToolTip btn txt
						)
						
						local tempBm = copy tex
						--close tex
						local fadePower = case texSlotSize.state of --adjust fade according to display size -> smaller = more fade
						(
							1: 0.5
							2: 0.33
							3: 0.15
						)
						fadeBitmap tempBm power:fadePower
						mxs2dotBmp tempBm &btn.BackgroundImage width:texBtnSize.x height:texBtnSize.y
						if thisID != 0 then texBtnsErrorState[thisID] = false
						
						gc light:true
					)
					else 
					(
						mxs2dotBmp (bitmap texBtnSize.x 4 color:(color 255 67 17)) &btn.BackgroundImage --set feedback to something different than file not found
						btnTooltip.SetToolTip btn ("FILE UNREADABLE\n" + filename)
						if thisID != 0 then texBtnsErrorState[thisID] = true
					)
				)
				else
				(
					--mxs2dotBmp (bitmap texBtnSize.x texBtnSize.y color:(color 179 51 51)) &btn.BackgroundImage
					btn.BackgroundImage = undefined
					btnTooltip.SetToolTip btn ("FILE NOT FOUND\n" + filename)
					if thisID != 0 then texBtnsErrorState[thisID] = true
				)
			)
			else
			(
				btn.BackgroundImage = undefined
				btnTooltip.SetToolTip btn ""
				if thisID != 0 then texBtnsErrorState[thisID] = false
			)
			setSlotBaseState btn --slot border is also used for error feedback
		)

		fn updateUiBmAll =
		(
			for texName in TexList do
			(
				local propertyName = texName + "Tex"
				if isProperty this propertyName then -- need to check weither property exists or not for removed ones.
				(
					updateUiBm texName
				)
			)
		)
		
		-- update tooltips flags
		fn updateUiFlags basename =
		(
			local filename = getProperty this (basename + "Tex")
			local btn = getProperty this.texturesUI (basename + "TexBtn")
			if filename != "" then
			(
				if getFullFilePath &filename then
				(
					local TFlagsFile = getFilenamePath filename + (filenameFromPath filename) + ".FLAGS"
					local TFlags = ""
					local stream = openFile TFlagsFile
					if stream != undefined then
					(
						TFlags = "TFlags:\n"
						TFlags += readDelimitedString stream #eof
						close stream
					)
					
					local txt = btnTooltip.GetToolTip btn
					local pos = findString txt "TFlags"
					if pos != undefined then
					(
						txt = (substring txt 1 (pos-1)) + TFlags
						btnTooltip.SetToolTip btn txt
					)
				)
			)
		)
		
		fn setupQuickPreviewState =
		(
			chkbtnQuickPreview.checked = MSFS2024_isTexturePreviewActive()
		)

		fn updateUI =
		(
			setupQuickPreviewState()
			updateTexSlots()
			updateUiBmAll()
		)
		
		on chkbtnQuickPreview changed state do
		(
			MSFS2024_setTexturePreviewActive state
		)
		
		on texSlotSize changed val do
		(
			texBtnSize.y = texSlotHeights[val]
			updateUI()
		)

		-- bitmaps loading
		fn loadTex filename basename =
		(
			local localHolding = false
			if (theHold.holding() == false) do
			(
				theHold.begin()
				localHolding = true
			)

			try
			(
				animate off
				(
					filename = pathConfig.convertPathToRelativeTo filename (pathConfig.getCurrentProjectFolder())
					setProperty this (basename + "Tex") filename
					updateUiBm basename

					if (theHold.holding() == true and localHolding) do
						theHold.accept ("Mtl : Load Texture" + " (" + basename + ")")
				)
			)
			catch
			(
				if (theHold.holding() == true and localHolding) do
					theHold.Cancel()
			)
		)

		-- bitmaps deleting
		fn clearTex basename =
		(
			local localHolding = false
			if (theHold.holding() == false) do
			(
				theHold.begin()
				localHolding = true
			)

			try
			(
				animate off
				(
					local tex = (basename + "Tex") as name
					setProperty this tex ""
					updateUiBm basename

					if (theHold.holding() == true and localHolding) do
						theHold.accept ("Mtl : Clear Texture" + " (" + basename + ")")
				)
			)
			catch
			(
				if (theHold.holding() == true and localHolding) do
					theHold.Cancel()
			)

			if(basename == "BlendMask") do
			(
				updateTexSlots()
				delegate.p_blendmaskEnabled = false
			)

			if(basename == "Dirt") do
			(
				updateTexSlots()
				delegate.p_dirtEnabled = false
			)

			if(basename == "FoliageMask") do (
				updateTexSlots()
				delegate.p_foliagemaskEnabled = false
			)

			if(basename == "DetailColor") do
			(
				updateTexSlots()
				delegate.p_detailColorEnabled = false
			)

			if(basename == "DetailNormal") do
			(
				updateTexSlots()
				delegate.p_detailNormalEnabled = false
			)

			if(basename == "DetailOcclusionRoughnessMetallic") do
			(
				updateTexSlots()
				delegate.p_detailOccRoughMetalEnabled = false
			)

			if(basename == "Occlusion") do
			(
				updateTexSlots()
				delegate.p_occlusionEnabled = false
			)
		)

		fn loadLinked filename basename =
		(			
			if basename == "BaseColor"  and filename!=undefined	then
			(				
				-- filename	=	(pathconfig.convertPathToAbsolute 	(pathconfig.appendpath 	(pathConfig.getCurrentProjectFolder())	filename	)	)
				local cpath = getFilenamePath filename
				local cname = getFilenameFile filename
				local ctype = getFilenameType filename
				local offset = findString (tolower cname) "albedo"


				if offset != undefined then		--		nommenclature 1 (airport)
				(
					cname = substring cname 1 (offset-1)
					local comp = pathConfig.appendPath cpath (cname + "COMP"+ctype)
					local nmap = pathConfig.appendPath cpath (cname + "Normal"+ctype)
					local	emiss = pathConfig.appendPath cpath (cname + "Emissive"+ctype)
					if this.NormalTex == "" and doesFileExist nmap then
						loadTex (pathConfig.convertPathToRelativeTo  nmap (pathConfig.getCurrentProjectFolder())) "Normal"
					if this.OcclusionRoughnessMetallicTex == "" and doesFileExist comp then
						loadTex (pathConfig.convertPathToRelativeTo  comp (pathConfig.getCurrentProjectFolder())) "OcclusionRoughnessMetallic"
					if this.EmissiveTex == "" and doesFileExist emiss then
						loadTex (pathConfig.convertPathToRelativeTo  emiss (pathConfig.getCurrentProjectFolder())) "Emissive"
				)
				else										--		nommenclature 2 (planes)
				(
					offset = findString (tolower  cname) "_albd"
					if offset != undefined then
					(
						cname = substring cname 1 (offset-1)
						local comp = pathConfig.appendPath cpath (cname + "_comp"+ctype)
						local nmap = pathConfig.appendPath cpath (cname + "_norm"+ctype)
						local	emiss = pathConfig.appendPath cpath (cname + "_emis"+ctype)
						if this.NormalTex == "" and doesFileExist nmap then
							loadTex (pathConfig.convertPathToRelativeTo  nmap (pathConfig.getCurrentProjectFolder())) "Normal"
						if this.OcclusionRoughnessMetallicTex == "" and doesFileExist comp then
							loadTex (pathConfig.convertPathToRelativeTo  comp (pathConfig.getCurrentProjectFolder())) "OcclusionRoughnessMetallic"
						if this.EmissiveTex == "" and doesFileExist emiss then
							loadTex (pathConfig.convertPathToRelativeTo  emiss (pathConfig.getCurrentProjectFolder())) "Emissive"
					)
				)
			)

			if(basename == "BlendMask") do
			(
				updateTexSlots()
			)
			
			if(basename == "FoliageMask") do
			(
				updateTexSlots()
			)

			if(basename == "TireDetails") do (
				updateTexSlots()
				delegate.p_tireDetailsEnabled = false
			)

			if(basename == "TireMudNormal") do (
				updateTexSlots()
				delegate.p_tireMudNormalEnabled = false
			)

			if(basename == "DetailColor") do
			(
				updateTexSlots()
				delegate.p_detailColorEnabled = true
			)

			if(basename == "DetailNormal") do
			(
				updateTexSlots()
				delegate.p_detailNormalEnabled = true
			)

			if(basename == "DetailOcclusionRoughnessMetallic") do
			(
				updateTexSlots()
				delegate.p_detailOccRoughMetalEnabled = true
			)
			
			if(basename == "Occlusion") do
			(
				updateTexSlots()
				delegate.p_occlusionEnabled = true
			)
		)

		fn browseTex basename caption: =
		(
			local curPath = getProperty this (basename + "Tex")
			if (curPath == "" or curPath == undefined) then curPath = (pathConfig.convertPathToAbsolute ".") + "\\"
				else curPath = pathConfig.convertPathToAbsolute curPath
			caoption = if caption != unsupplied then caption else basename
			local filename = getOpenFileName caption:caption filename:curPath historyCategory:"MSFS2024History" types:filesTypes
			if filename != undefined then
				loadTex 	filename basename
				loadLinked	filename basename

			if(basename == "BlendMask") do
			(
				updateTexSlots()
			)
			
			if(basename == "FoliageMask") do
			(
				updateTexSlots()
			)

			if(basename == "DetailColor") do
			(
				updateTexSlots()
				delegate.p_detailColorEnabled = true
			)

			if(basename == "DetailNormal") do
			(
				updateTexSlots()
				delegate.p_detailNormalEnabled = true
			)

			if(basename == "DetailOcclusionRoughnessMetallic") do
			(
				updateTexSlots()
				delegate.p_detailOccRoughMetalEnabled = true
			)
			
			if(basename == "Occlusion") do
			(
				updateTexSlots()
				delegate.p_occlusionEnabled = true
			)
		)

		-- right clic menu
		fn rightclickMenu basename =
		(
			activeTex = basename --couldn't send that to the popupmenu ?
			popUpMenu MSFS2024MaterialRCMenuTex
		)

		local mdist = 0.0
		local oldPos = [0.0, 0.0]
		fn btnDragMove sender arg basename =
		(
			local pos = [arg.location.x, arg.location.y]
			if arg.button==arg.button.left then
			(
				mdist += distance pos oldPos
				if mdist>10.0 do
				(
					local filename = getProperty this (basename + "Tex")
					if filename != undefined and filename != "" do
						sender.DoDragDrop #("MSFS2024MaterialDnD",basename,filename) (dotNetClass "System.Windows.Forms.DragDropEffects").Move
				)
			)
			else
			(
				mdist = 0.0
			)
			oldPos = pos
		)

		fn btnDragOver sender arg =
		(
			arg.Effect = arg.Effect.Move
		)

		fn btnDragDrop arg basename =
		(
			--print (arg.data.GetFormats())
			local data = arg.data.GetData "FileNameW"
			if data != undefined then
			(
				local filename = data[1]
				if filename!=undefined then
				(
					local ext = "*" + getFilenameType filename + "*"
					if matchPattern filesTypes pattern:ext ignoreCase:true and ext!="**" then
					(
						loadTex 		filename basename
						loadLinked	filename basename
					)
				)
			)
			else
			(
				data = arg.data.GetData "System.Object[]"
				if data != undefined and data[1]=="MSFS2024MaterialDnD" do --swap
				(
					local localHolding = false
					if (theHold.holding() == false) do
					(
						theHold.begin()
						localHolding = true
					)

					try
					(
						local filename = getProperty this (basename + "Tex")
						local srcBasename = data[2]
						local srcFilename = data[3]

						if filename != "" then
							loadTex filename srcBasename
						else
							clearTex srcBasename

						loadTex srcFilename basename

						if (theHold.holding() == true and localHolding) do
							theHold.accept ("Mtl : Swap Textures " + "(" + srcBasename + " / " + basename + ")")
					)
					catch
					(
						if (theHold.holding() == true and localHolding) do
							theHold.Cancel()
					)
				)
			)
		)
		
		on btnReloadUI pressed do updateUI()
		
		on btnClearAllSlots pressed do
		(
			for n in TexList do clearTex n
		)
		
		-- add caption arg to help user see what texture they browse for
		on BaseColorTexBtn							MouseClick sender arg do browseTex "BaseColor"
		on OcclusionRoughnessMetallicTexBtn			MouseClick sender arg do browseTex "OcclusionRoughnessMetallic"
		on NormalTexBtn								MouseClick sender arg do browseTex "Normal"
		on BlendMaskTexBtn							MouseClick sender arg do browseTex "BlendMask"
		on FoliageMaskTexBtn						MouseClick sender arg do browseTex "FoliageMask"
		on DirtTexBtn								MouseClick sender arg do browseTex "Dirt"
		on DirtOcclusionRoughnessMetallicTexBtn		MouseClick sender arg do browseTex "DirtOcclusionRoughnessMetallic"
		on WetnessAOTexBtn							MouseClick sender arg do browseTex "WetnessAO"
		on WindshieldDetailNormalTexBtn				MouseClick sender arg do browseTex "WindshieldDetailNormal"
		on ScratchesNormalTexBtn					MouseClick sender arg do browseTex "ScratchesNormal"
		on WiperMaskTexBtn							MouseClick sender arg do browseTex "WiperMask"
		on AnisoDirectionRoughnessTexBtn			MouseClick sender arg do browseTex "AnisoDirectionRoughness"
		on OpacityTexBtn							MouseClick sender arg do browseTex "Opacity"
		on EmissiveTexBtn							MouseClick sender arg do browseTex "Emissive"
		on DetailColorTexBtn						MouseClick sender arg do browseTex "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn	MouseClick sender arg do browseTex "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn						MouseClick sender arg do browseTex "DetailNormal"
		on OcclusionTexBtn							MouseClick sender arg do browseTex "Occlusion"
		on ClearcoatColorRoughnessTexBtn			MouseClick sender arg do browseTex "ClearcoatColorRoughness"
		on ClearcoatNormalTexBtn					MouseClick sender arg do browseTex "ClearcoatNormal"
		on IridescentThicknessTexBtn				MouseClick sender arg do browseTex "IridescentThickness"
		on WindshieldInsectsTexBtn					MouseClick sender arg do browseTex "WindshieldInsects"
		on WindshieldInsectsMaskTexBtn				MouseClick sender arg do browseTex "WindshieldInsectsMask"
		on TireDetailsTexBtn						MouseClick sender arg do browseTex "TireDetails"
		on TireMudNormalTexBtn						MouseClick sender arg do browseTex "TireMudNormal"
		/*on PHPIInteriorHallwayAlbedoTexBtn			MouseClick sender arg do browseTex "PHPIInteriorHallwayAlbedo"			caption:"Interior Hallway Albedo"
		on PHPIInteriorHallwayNormalAoTexBtn		MouseClick sender arg do browseTex "PHPIInteriorHallwayNormalAo"		caption:"Interior Hallway Normal + AO"
		on PHPIInteriorHallwayEmissiveTexBtn		MouseClick sender arg do browseTex "PHPIInteriorHallwayEmissive"		caption:"Interior Hallway Emissive"
		on PHPIInteriorLeftWallAlbedoTexBtn			MouseClick sender arg do browseTex "PHPIInteriorLeftWallAlbedo"			caption:"Interior Left Wall Albedo"
		on PHPIInteriorLeftWallNormalAoTexBtn		MouseClick sender arg do browseTex "PHPIInteriorLeftWallNormalAo"		caption:"Interior Left Wall Normal + AO"
		on PHPIInteriorLeftWallEmissiveTexBtn		MouseClick sender arg do browseTex "PHPIInteriorLeftWallEmissive"		caption:"Interior Left Wall Emissive"
		on PHPIInteriorRightWallAlbedoTexBtn		MouseClick sender arg do browseTex "PHPIInteriorRightWallAlbedo"		caption:"Interior Right Wall Albedo"
		on PHPIInteriorRightWallNormalAoTexBtn		MouseClick sender arg do browseTex "PHPIInteriorRightWallNormalAo"		caption:"Interior Right Wall Normal + AO"
		on PHPIInteriorRightWallEmissiveTexBtn		MouseClick sender arg do browseTex "PHPIInteriorRightWallEmissive"		caption:"Interior Right Wall Emissive"
		on PHPISideProjectionAlbedoHeightTexBtn		MouseClick sender arg do browseTex "PHPISideProjectionAlbedoHeight"		caption:"Projection Side Albedo + Height"
		on PHPISideProjectionNormalAoTexBtn			MouseClick sender arg do browseTex "PHPISideProjectionNormalAo"			caption:"Projection Side Normal + AO"
		on PHPISideProjectionEmissiveTexBtn			MouseClick sender arg do browseTex "PHPISideProjectionEmissive"			caption:"Projection Side Emissive"
		on PHPIFrontProjectionAlbedoHeightTexBtn	MouseClick sender arg do browseTex "PHPIFrontProjectionAlbedoHeight"	caption:"Projection Front Albedo + Height"
		on PHPIFrontProjectionNormalAoTexBtn		MouseClick sender arg do browseTex "PHPIFrontProjectionNormalAo"		caption:"Projection Front Normal + AO"
		on PHPIFrontProjectionEmissiveTexBtn		MouseClick sender arg do browseTex "PHPIFrontProjectionEmissive"		caption:"Projection Front Emissive"
		on PHPIBackProjectionAlbedoHeightTexBtn		MouseClick sender arg do browseTex "PHPIBackProjectionAlbedoHeight"		caption:"Projection Back Albedo + Height"
		on PHPIBackProjectionNormalAoTexBtn			MouseClick sender arg do browseTex "PHPIBackProjectionNormalAo"			caption:"Projection Back Normal + AO"
		on PHPIBackProjectionEmissiveTexBtn			MouseClick sender arg do browseTex "PHPIBackProjectionEmissive"			caption:"Projection Back Emissive"
		on PHPITopProjectionAlbedoHeightTexBtn		MouseClick sender arg do browseTex "PHPITopProjectionAlbedoHeight"		caption:"Projection Top Albedo + Height"
		on PHPITopProjectionNormalAoTexBtn			MouseClick sender arg do browseTex "PHPITopProjectionNormalAo"			caption:"Projection Top Normal + AO"
		on PHPITopProjectionEmissiveTexBtn			MouseClick sender arg do browseTex "PHPITopProjectionEmissive"			caption:"Projection Top Emissive"*/

		on BaseColorTexBtn							MouseMove sender arg do btnDragMove sender arg "BaseColor"
		on OcclusionRoughnessMetallicTexBtn			MouseMove sender arg do btnDragMove sender arg "OcclusionRoughnessMetallic"
		on NormalTexBtn								MouseMove sender arg do btnDragMove sender arg "Normal"
		on BlendMaskTexBtn							MouseMove sender arg do btnDragMove sender arg "BlendMask"
		on FoliageMaskTexBtn						MouseMove sender arg do btnDragMove sender arg "FoliageMask"
		on WetnessAOTexBtn							MouseMove sender arg do btnDragMove sender arg "WetnessAO"
		on WindshieldDetailNormalTexBtn				MouseMove sender arg do btnDragMove sender arg "WindshieldDetailNormal"
		on ScratchesNormalTexBtn					MouseMove sender arg do btnDragMove sender arg "ScratchesNormal"
		on WiperMaskTexBtn							MouseMove sender arg do btnDragMove sender arg "WiperMask"
		on AnisoDirectionRoughnessTexBtn			MouseMove sender arg do btnDragMove sender arg "AnisoDirectionRoughness"
		on DirtTexBtn								MouseMove sender arg do btnDragMove sender arg "Dirt"
		on OpacityTexBtn							MouseMove sender arg do btnDragMove sender arg "Opacity"
		on EmissiveTexBtn							MouseMove sender arg do btnDragMove sender arg "Emissive"
		on DetailColorTexBtn						MouseMove sender arg do btnDragMove sender arg "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn	MouseMove sender arg do btnDragMove sender arg "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn						MouseMove sender arg do btnDragMove sender arg "DetailNormal"
		on OcclusionTexBtn							MouseMove sender arg do btnDragMove sender arg "Occlusion"
		on ClearcoatColorRoughnessTexBtn			MouseMove sender arg do btnDragMove sender arg "ClearcoatColorRoughness"
		on ClearcoatNormalTexBtn					MouseMove sender arg do btnDragMove sender arg "ClearcoatNormal"
		on IridescentThicknessTexBtn				MouseMove sender arg do btnDragMove sender arg "IridescentThickness"
		on WindshieldInsectsTexBtn					MouseMove sender arg do btnDragMove sender arg "WindshieldInsects"
		on WindshieldInsectsMaskTexBtn				MouseMove sender arg do btnDragMove sender arg "WindshieldInsectsMask"
		on DirtOcclusionRoughnessMetallicTexBtn		MouseMove sender arg do btnDragMove sender arg "DirtOcclusionRoughnessMetallic"
		on TireDetailsTexBtn						MouseMove sender arg do btnDragMove sender arg "TireDetails"
		on TireMudNormalTexBtn						MouseMove sender arg do btnDragMove sender arg "TireMudNormal"
		/*on PHPIInteriorHallwayAlbedoTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPIInteriorHallwayAlbedo"
		on PHPIInteriorHallwayNormalAoTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorHallwayNormalAo"
		on PHPIInteriorHallwayEmissiveTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorHallwayEmissive"
		on PHPIInteriorLeftWallAlbedoTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPIInteriorLeftWallAlbedo"
		on PHPIInteriorLeftWallNormalAoTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorLeftWallNormalAo"
		on PHPIInteriorLeftWallEmissiveTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorLeftWallEmissive"
		on PHPIInteriorRightWallAlbedoTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorRightWallAlbedo"
		on PHPIInteriorRightWallNormalAoTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorRightWallNormalAo"
		on PHPIInteriorRightWallEmissiveTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIInteriorRightWallEmissive"
		on PHPISideProjectionAlbedoHeightTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPISideProjectionAlbedoHeight"
		on PHPISideProjectionNormalAoTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPISideProjectionNormalAo"
		on PHPISideProjectionEmissiveTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPISideProjectionEmissive"
		on PHPIFrontProjectionAlbedoHeightTexBtn	MouseMove sender arg do btnDragMove sender arg "PHPIFrontProjectionAlbedoHeight"
		on PHPIFrontProjectionNormalAoTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIFrontProjectionNormalAo"
		on PHPIFrontProjectionEmissiveTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIFrontProjectionEmissive"
		on PHPIBackProjectionAlbedoHeightTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPIBackProjectionAlbedoHeight"
		on PHPIBackProjectionNormalAoTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPIBackProjectionNormalAo"
		on PHPIBackProjectionEmissiveTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPIBackProjectionEmissive"
		on PHPITopProjectionAlbedoHeightTexBtn		MouseMove sender arg do btnDragMove sender arg "PHPITopProjectionAlbedoHeight"
		on PHPITopProjectionNormalAoTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPITopProjectionNormalAo"
		on PHPITopProjectionEmissiveTexBtn			MouseMove sender arg do btnDragMove sender arg "PHPITopProjectionEmissive"*/

		on BaseColorTexBtn							DragOver sender arg do btnDragOver sender arg
		on OcclusionRoughnessMetallicTexBtn			DragOver sender arg do btnDragOver sender arg
		on NormalTexBtn								DragOver sender arg do btnDragOver sender arg
		on BlendMaskTexBtn							DragOver sender arg do btnDragOver sender arg
		on FoliageMaskTexBtn						DragOver sender arg do btnDragOver sender arg
		on DirtTexBtn								DragOver sender arg do btnDragOver sender arg
		on DirtOcclusionRoughnessMetallicTexBtn 	DragOver sender arg do btnDragOver sender arg
		on WetnessAOTexBtn							DragOver sender arg do btnDragOver sender arg
		on WindshieldDetailNormalTexBtn				DragOver sender arg do btnDragOver sender arg
		on ScratchesNormalTexBtn					DragOver sender arg do btnDragOver sender arg
		on WiperMaskTexBtn							DragOver sender arg do btnDragOver sender arg
		on AnisoDirectionRoughnessTexBtn			DragOver sender arg do btnDragOver sender arg
		on OpacityTexBtn							DragOver sender arg do btnDragOver sender arg
		on EmissiveTexBtn							DragOver sender arg do btnDragOver sender arg
		on DetailColorTexBtn						DragOver sender arg do btnDragOver sender arg
		on DetailOcclusionRoughnessMetallicTexBtn	DragOver sender arg do btnDragOver sender arg
		on DetailNormalTexBtn						DragOver sender arg do btnDragOver sender arg
		on OcclusionTexBtn							DragOver sender arg do btnDragOver sender arg
		on ClearcoatColorRoughnessTexBtn			DragOver sender arg do btnDragOver sender arg
		on ClearcoatNormalTexBtn					DragOver sender arg do btnDragOver sender arg
		on IridescentThicknessTexBtn				DragOver sender arg do btnDragOver sender arg
		on WindshieldInsectsTexBtn					DragOver sender arg do btnDragOver sender arg
		on WindshieldInsectsMaskTexBtn				DragOver sender arg do btnDragOver sender arg
		on TireDetailsTexBtn						DragOver sender arg do btnDragOver sender arg
		on TireMudNormalTexBtn						DragOver sender arg do btnDragOver sender arg
		/*on PHPIInteriorHallwayAlbedoTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorHallwayNormalAoTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorHallwayEmissiveTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorLeftWallAlbedoTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorLeftWallNormalAoTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorLeftWallEmissiveTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorRightWallAlbedoTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorRightWallNormalAoTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIInteriorRightWallEmissiveTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPISideProjectionAlbedoHeightTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPISideProjectionNormalAoTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPISideProjectionEmissiveTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPIFrontProjectionAlbedoHeightTexBtn	DragOver sender arg do btnDragOver sender arg
		on PHPIFrontProjectionNormalAoTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIFrontProjectionEmissiveTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIBackProjectionAlbedoHeightTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPIBackProjectionNormalAoTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPIBackProjectionEmissiveTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPITopProjectionAlbedoHeightTexBtn		DragOver sender arg do btnDragOver sender arg
		on PHPITopProjectionNormalAoTexBtn			DragOver sender arg do btnDragOver sender arg
		on PHPITopProjectionEmissiveTexBtn			DragOver sender arg do btnDragOver sender arg*/

		on BaseColorTexBtn							DragDrop sender arg do btnDragDrop arg "BaseColor"
		on OcclusionRoughnessMetallicTexBtn			DragDrop sender arg do btnDragDrop arg "OcclusionRoughnessMetallic"
		on NormalTexBtn								DragDrop sender arg do btnDragDrop arg "Normal"
		on BlendMaskTexBtn							DragDrop sender arg do btnDragDrop arg "BlendMask"
		on FoliageMaskTexBtn						DragDrop sender arg do btnDragDrop arg "FoliageMask"
		on DirtTexBtn								DragDrop sender arg do btnDragDrop arg "Dirt"
		on DirtOcclusionRoughnessMetallicTexBtn 	DragDrop sender arg do btnDragDrop arg "DirtOcclusionRoughnessMetallic"
		on WetnessAOTexBtn							DragDrop sender arg do btnDragDrop arg "WetnessAO"
		on WindshieldDetailNormalTexBtn				DragDrop sender arg do btnDragDrop arg "WindshieldDetailNormal"
		on ScratchesNormalTexBtn					DragDrop sender arg do btnDragDrop arg "ScratchesNormal"
		on WiperMaskTexBtn							DragDrop sender arg do btnDragDrop arg "WiperMask"
		on AnisoDirectionRoughnessTexBtn			DragDrop sender arg do btnDragDrop arg "AnisoDirectionRoughness"
		on OpacityTexBtn							DragDrop sender arg do btnDragDrop arg "Opacity"
		on EmissiveTexBtn							DragDrop sender arg do btnDragDrop arg "Emissive"
		on DetailColorTexBtn						DragDrop sender arg do btnDragDrop arg "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn	DragDrop sender arg do btnDragDrop arg "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn						DragDrop sender arg do btnDragDrop arg "DetailNormal"
		on OcclusionTexBtn							DragDrop sender arg do btnDragDrop arg "Occlusion"
		on ClearcoatColorRoughnessTexBtn			DragDrop sender arg do btnDragDrop arg "ClearcoatColorRoughness"
		on ClearcoatNormalTexBtn					DragDrop sender arg do btnDragDrop arg "ClearcoatNormal"
		on IridescentThicknessTexBtn				DragDrop sender arg do btnDragDrop arg "IridescentThickness"
		on WindshieldInsectsTexBtn					DragDrop sender arg do btnDragDrop arg "WindshieldInsects"
		on WindshieldInsectsMaskTexBtn				DragDrop sender arg do btnDragDrop arg "WindshieldInsectsMask"
		on TireDetailsTexBtn						DragDrop sender arg do btnDragDrop arg "TireDetails"
		on TireMudNormalTexBtn						DragDrop sender arg do btnDragDrop arg "TireMudNormal"
		/*on PHPIInteriorHallwayAlbedoTexBtn			DragDrop sender arg do btnDragDrop arg "PHPIInteriorHallwayAlbedo"
		on PHPIInteriorHallwayNormalAoTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorHallwayNormalAo"
		on PHPIInteriorHallwayEmissiveTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorHallwayEmissive"
		on PHPIInteriorLeftWallAlbedoTexBtn			DragDrop sender arg do btnDragDrop arg "PHPIInteriorLeftWallAlbedo"
		on PHPIInteriorLeftWallNormalAoTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorLeftWallNormalAo"
		on PHPIInteriorLeftWallEmissiveTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorLeftWallEmissive"
		on PHPIInteriorRightWallAlbedoTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorRightWallAlbedo"
		on PHPIInteriorRightWallNormalAoTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorRightWallNormalAo"
		on PHPIInteriorRightWallEmissiveTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIInteriorRightWallEmissive"
		on PHPISideProjectionAlbedoHeightTexBtn		DragDrop sender arg do btnDragDrop arg "PHPISideProjectionAlbedoHeight"
		on PHPISideProjectionNormalAoTexBtn			DragDrop sender arg do btnDragDrop arg "PHPISideProjectionNormalAo"
		on PHPISideProjectionEmissiveTexBtn			DragDrop sender arg do btnDragDrop arg "PHPISideProjectionEmissive"
		on PHPIFrontProjectionAlbedoHeightTexBtn	DragDrop sender arg do btnDragDrop arg "PHPIFrontProjectionAlbedoHeight"
		on PHPIFrontProjectionNormalAoTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIFrontProjectionNormalAo"
		on PHPIFrontProjectionEmissiveTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIFrontProjectionEmissive"
		on PHPIBackProjectionAlbedoHeightTexBtn		DragDrop sender arg do btnDragDrop arg "PHPIBackProjectionAlbedoHeight"
		on PHPIBackProjectionNormalAoTexBtn			DragDrop sender arg do btnDragDrop arg "PHPIBackProjectionNormalAo"
		on PHPIBackProjectionEmissiveTexBtn			DragDrop sender arg do btnDragDrop arg "PHPIBackProjectionEmissive"
		on PHPITopProjectionAlbedoHeightTexBtn		DragDrop sender arg do btnDragDrop arg "PHPITopProjectionAlbedoHeight"
		on PHPITopProjectionNormalAoTexBtn			DragDrop sender arg do btnDragDrop arg "PHPITopProjectionNormalAo"
		on PHPITopProjectionEmissiveTexBtn			DragDrop sender arg do btnDragDrop arg "PHPITopProjectionEmissive"*/

		on BaseColorTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "BaseColor"
		on OcclusionRoughnessMetallicTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "OcclusionRoughnessMetallic"
		on NormalTexBtn								mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "Normal"
		on BlendMaskTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "BlendMask"
		on FoliageMaskTexBtn						mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "FoliageMask"
		on DirtTexBtn								mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "Dirt"
		on DirtOcclusionRoughnessMetallicTexBtn 	mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "DirtOcclusionRoughnessMetallic"
		on WetnessAOTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "WetnessAO"
		on WindshieldDetailNormalTexBtn				mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "WindshieldDetailNormal"
		on ScratchesNormalTexBtn					mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "ScratchesNormal"
		on WiperMaskTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "WiperMask"
		on AnisoDirectionRoughnessTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "AnisoDirectionRoughness"
		on OpacityTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "Opacity"
		on EmissiveTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "Emissive"
		on DetailColorTexBtn						mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn	mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn						mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "DetailNormal"
		on OcclusionTexBtn							mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "Occlusion"
		on ClearcoatColorRoughnessTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "ClearcoatColorRoughness"
		on ClearcoatNormalTexBtn					mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "ClearcoatNormal"
		on IridescentThicknessTexBtn				mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "IridescentThickness"
		on WindshieldInsectsTexBtn					mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "WindshieldInsects"
		on WindshieldInsectsMaskTexBtn				mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "WindshieldInsectsMask"
		on TireDetailsTexBtn						mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "TireDetails"
		on TireMudNormalTexBtn						mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "TireMudNormal"
		/*on PHPIInteriorHallwayAlbedoTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorHallwayAlbedo"
		on PHPIInteriorHallwayNormalAoTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorHallwayNormalAo"
		on PHPIInteriorHallwayEmissiveTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorHallwayEmissive"
		on PHPIInteriorLeftWallAlbedoTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorLeftWallAlbedo"
		on PHPIInteriorLeftWallNormalAoTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorLeftWallNormalAo"
		on PHPIInteriorLeftWallEmissiveTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorLeftWallEmissive"
		on PHPIInteriorRightWallAlbedoTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorRightWallAlbedo"
		on PHPIInteriorRightWallNormalAoTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorRightWallNormalAo"
		on PHPIInteriorRightWallEmissiveTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIInteriorRightWallEmissive"
		on PHPISideProjectionAlbedoHeightTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPISideProjectionAlbedoHeight"
		on PHPISideProjectionNormalAoTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPISideProjectionNormalAo"
		on PHPISideProjectionEmissiveTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPISideProjectionEmissive"
		on PHPIFrontProjectionAlbedoHeightTexBtn	mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIFrontProjectionAlbedoHeight"
		on PHPIFrontProjectionNormalAoTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIFrontProjectionNormalAo"
		on PHPIFrontProjectionEmissiveTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIFrontProjectionEmissive"
		on PHPIBackProjectionAlbedoHeightTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIBackProjectionAlbedoHeight"
		on PHPIBackProjectionNormalAoTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIBackProjectionNormalAo"
		on PHPIBackProjectionEmissiveTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPIBackProjectionEmissive"
		on PHPITopProjectionAlbedoHeightTexBtn		mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPITopProjectionAlbedoHeight"
		on PHPITopProjectionNormalAoTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPITopProjectionNormalAo"
		on PHPITopProjectionEmissiveTexBtn			mouseUp sender arg do if arg.button==arg.button.right do rightclickMenu "PHPITopProjectionEmissive"*/
		
		on BaseColorTexBtn							mouseHover sender arg do setSlotHoverState sender "BaseColor"
		on OcclusionRoughnessMetallicTexBtn			mouseHover sender arg do setSlotHoverState sender "OcclusionRoughnessMetallic"
		on NormalTexBtn								mouseHover sender arg do setSlotHoverState sender "Normal"
		on BlendMaskTexBtn							mouseHover sender arg do setSlotHoverState sender "BlendMask"
		on FoliageMaskTexBtn						mouseHover sender arg do setSlotHoverState sender "FoliageMask"
		on DirtTexBtn								mouseHover sender arg do setSlotHoverState sender "Dirt"
		on DirtOcclusionRoughnessMetallicTexBtn		mouseHover sender arg do setSlotHoverState sender "DirtOcclusionRoughnessMetallic"
		on WetnessAOTexBtn							mouseHover sender arg do setSlotHoverState sender "WetnessAO"
		on WindshieldDetailNormalTexBtn				mouseHover sender arg do setSlotHoverState sender "WindshieldDetailNormal"
		on ScratchesNormalTexBtn					mouseHover sender arg do setSlotHoverState sender "ScratchesNormal"
		on WiperMaskTexBtn							mouseHover sender arg do setSlotHoverState sender "WiperMask"
		on AnisoDirectionRoughnessTexBtn			mouseHover sender arg do setSlotHoverState sender "AnisoDirectionRoughness"
		on OpacityTexBtn							mouseHover sender arg do setSlotHoverState sender "Opacity"
		on EmissiveTexBtn							mouseHover sender arg do setSlotHoverState sender "Emissive"
		on DetailColorTexBtn						mouseHover sender arg do setSlotHoverState sender "DetailColor"
		on DetailOcclusionRoughnessMetallicTexBtn	mouseHover sender arg do setSlotHoverState sender "DetailOcclusionRoughnessMetallic"
		on DetailNormalTexBtn						mouseHover sender arg do setSlotHoverState sender "DetailNormal"
		on OcclusionTexBtn							mouseHover sender arg do setSlotHoverState sender "Occlusion"
		on ClearcoatColorRoughnessTexBtn			mouseHover sender arg do setSlotHoverState sender "ClearcoatColorRoughness"
		on ClearcoatNormalTexBtn					mouseHover sender arg do setSlotHoverState sender "ClearcoatNormal"
		on IridescentThicknessTexBtn				mouseHover sender arg do setSlotHoverState sender "IridescentThickness"
		on WindshieldInsectsTexBtn					mouseHover sender arg do setSlotHoverState sender "WindshieldInsects"
		on WindshieldInsectsMaskTexBtn				mouseHover sender arg do setSlotHoverState sender "WindshieldInsectsMask"
		on TireDetailsTexBtn						mouseHover sender arg do setSlotHoverState sender "TireDetails"
		on TireMudNormalTexBtn						mouseHover sender arg do setSlotHoverState sender "TireMudNormal"
		/*on PHPIInteriorHallwayAlbedoTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPIInteriorHallwayAlbedo"
		on PHPIInteriorHallwayNormalAoTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorHallwayNormalAo"
		on PHPIInteriorHallwayEmissiveTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorHallwayEmissive"
		on PHPIInteriorLeftWallAlbedoTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPIInteriorLeftWallAlbedo"
		on PHPIInteriorLeftWallNormalAoTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorLeftWallNormalAo"
		on PHPIInteriorLeftWallEmissiveTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorLeftWallEmissive"
		on PHPIInteriorRightWallAlbedoTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorRightWallAlbedo"
		on PHPIInteriorRightWallNormalAoTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorRightWallNormalAo"
		on PHPIInteriorRightWallEmissiveTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIInteriorRightWallEmissive"
		on PHPISideProjectionAlbedoHeightTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPISideProjectionAlbedoHeight"
		on PHPISideProjectionNormalAoTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPISideProjectionNormalAo"
		on PHPISideProjectionEmissiveTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPISideProjectionEmissive"
		on PHPIFrontProjectionAlbedoHeightTexBtn	mouseHover sender arg do setSlotHoverState sender "PHPIFrontProjectionAlbedoHeight"
		on PHPIFrontProjectionNormalAoTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIFrontProjectionNormalAo"
		on PHPIFrontProjectionEmissiveTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIFrontProjectionEmissive"
		on PHPIBackProjectionAlbedoHeightTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPIBackProjectionAlbedoHeight"
		on PHPIBackProjectionNormalAoTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPIBackProjectionNormalAo"
		on PHPIBackProjectionEmissiveTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPIBackProjectionEmissive"
		on PHPITopProjectionAlbedoHeightTexBtn		mouseHover sender arg do setSlotHoverState sender "PHPITopProjectionAlbedoHeight"
		on PHPITopProjectionNormalAoTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPITopProjectionNormalAo"
		on PHPITopProjectionEmissiveTexBtn			mouseHover sender arg do setSlotHoverState sender "PHPITopProjectionEmissive"*/

		on BaseColorTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on OcclusionRoughnessMetallicTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on NormalTexBtn								mouseLeave sender arg do setSlotBaseState sender
		on BlendMaskTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on FoliageMaskTexBtn						mouseLeave sender arg do setSlotBaseState sender
		on DirtTexBtn								mouseLeave sender arg do setSlotBaseState sender
		on DirtOcclusionRoughnessMetallicTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on WetnessAOTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on WindshieldDetailNormalTexBtn				mouseLeave sender arg do setSlotBaseState sender
		on ScratchesNormalTexBtn					mouseLeave sender arg do setSlotBaseState sender
		on WiperMaskTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on AnisoDirectionRoughnessTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on OpacityTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on EmissiveTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on DetailColorTexBtn						mouseLeave sender arg do setSlotBaseState sender
		on DetailOcclusionRoughnessMetallicTexBtn	mouseLeave sender arg do setSlotBaseState sender
		on DetailNormalTexBtn						mouseLeave sender arg do setSlotBaseState sender
		on OcclusionTexBtn							mouseLeave sender arg do setSlotBaseState sender
		on ClearcoatColorRoughnessTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on ClearcoatNormalTexBtn					mouseLeave sender arg do setSlotBaseState sender
		on IridescentThicknessTexBtn				mouseLeave sender arg do setSlotBaseState sender
		on WindshieldInsectsTexBtn					mouseLeave sender arg do setSlotBaseState sender
		on WindshieldInsectsMaskTexBtn				mouseLeave sender arg do setSlotBaseState sender
		on TireDetailsTexBtn						mouseLeave sender arg do setSlotBaseState sender
		on TireMudNormalTexBtn						mouseLeave sender arg do setSlotBaseState sender
		/*on PHPIInteriorHallwayAlbedoTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorHallwayNormalAoTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorHallwayEmissiveTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorLeftWallAlbedoTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorLeftWallNormalAoTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorLeftWallEmissiveTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorRightWallAlbedoTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorRightWallNormalAoTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIInteriorRightWallEmissiveTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPISideProjectionAlbedoHeightTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPISideProjectionNormalAoTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPISideProjectionEmissiveTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPIFrontProjectionAlbedoHeightTexBtn	mouseLeave sender arg do setSlotBaseState sender
		on PHPIFrontProjectionNormalAoTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIFrontProjectionEmissiveTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIBackProjectionAlbedoHeightTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPIBackProjectionNormalAoTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPIBackProjectionEmissiveTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPITopProjectionAlbedoHeightTexBtn		mouseLeave sender arg do setSlotBaseState sender
		on PHPITopProjectionNormalAoTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPITopProjectionEmissiveTexBtn			mouseLeave sender arg do setSlotBaseState sender
		on PHPITopProjectionEmissiveTexBtn			mouseLeave sender arg do setSlotBaseState sender*/
		
		on texturesUI open do
		(
			if texBtnsPos == undefined then texBtnsPos = for o in texBtns collect o.pos
			if texBtnsErrorState == undefined then texBtnsErrorState = for o in texBtns collect false
			initTextureSlots()
			texturesUI.open = MSFS2024_texturesRolledUp
			if not loading and this.delegate != undefined then --"loading" send true before that the delegate is defined
			(
				updateUI()
			)
		)

		on texturesUI rolledUp state do
		(
			MSFS2024_texturesRolledUp = state
		)

		on texturesUI reload do
		(
			if this.delegate != undefined then  --"loading" send true before that the delegate is defined
			(
				updateUI()
			)
		)
	)
	
	on create do
	(
		loadShader()
		createControllers()
		-- delegate.renderMaterial = undefined -- this make 3dsmax crash in max2021
	)

	on postCreate do
	(
	)

	on clone original do
	(
		Assembly = dotNetClass "System.Reflection.Assembly"
		dllPath = symbolicPaths.getPathValue(1) + "\bin\assemblies\MSFS2024_Max2Babylon.dll"
    	Assembly.loadfrom dllPath
		maxScriptManager = dotNetObject "MSFS2024_Max2Babylon.MaxScriptManager"
		anim_handle = getHandleByAnim this
		maxScriptManager.initGUID(anim_handle) 
	)
	
	on load do
	(
		loadShader()
		loadControllers()
	)

	on postLoad do
	(
		if bApplyPhotometricScale do
		(
			print "Scale MSFS2024_Material to Photometric range"
			emissiveMul *= 200.0
			bApplyPhotometricScale = false
		)
	)

	on update do
	(
		-- Do not set parameters here, shaders paths have not been updated yet,
		-- which will lead to shader paramters errors if the path have changed
		-- Can't we set parameters without calling set handlers ?
		MatEditor.close()
		if version < 2 do
		(
			bApplyPhotometricScale = true
		)
	)
)

callbacks.removeScripts id:#MSFS2024_MaterialCallback

callbacks.addScript #sceneUndo \
"local undoStr = callbacks.notificationParam()
if MatEditor.isOpen() then
(
	local mat = medit.GetCurMtl()
	if classof mat == MSFS2024_Material then
		mat.updateGlobalUI()
)
" id:#MSFS2024_MaterialCallback

callbacks.addScript #sceneRedo \
"local undoStr = callbacks.notificationParam()
if MatEditor.isOpen() then
(
	local mat = medit.GetCurMtl()
	if classof mat == MSFS2024_Material then
		mat.updateGlobalUI()
)
" id:#MSFS2024_MaterialCallback
