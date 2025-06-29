/*
TODO
- set white BG for AO rendering (do not use backplane here)
- proper texture bleed! (dotnet?) (if so, white BG for AO becomes less useful)
- file merge delete used
- proper file exists pre-check
*/

struct asobo_planeSeatProjStruct
(
	/* UX OUTPUT */
	fn getErrorMessage c &title &isError defaultTitle: debugExtraTxt:"-??-" =
	(
		if title == unsupplied or title == undefined then
		(
			case c of
			(
				#unsupportedFileFormat:		title = "Unable to save files using this file format"
				#projectionComplete:		title = "Finished!"
				#projectionCancelled:		title = "Canceled!"
				default:					title = if defaultTitle != unsupplied then defaultTitle else "!"
			)
		)
		case c of
		(
			#noValidObjectSelected: 	(isError=true;	"Please select at least one geometry object to render.")
			#noValidSavePath: 			(isError=true;	"Please select where to save textures first.")
			#noValidSaveFile: 			(isError=true;	"Please check file name and type (need: name.extension).")
			#unsupportedFileFormat:		(isError=true;	debugExtraTxt+" file format is not supported.\nOnly supported format is:\n\tTiff Image File (*.tif)\n\nPlease choose *.tif file format when saving")
			#fileFormatSetupFail:		(isError=true;	"ERROR: couldn't properly setup "+debugExtraTxt+" file format")
			#fileOverwrite: 			(isError=true;	"One or more file(s) will be overwritten!")
			#cantCreateFolder:			(isError=true;	"ERROR: can't create folder \""+debugExtraTxt+"\"")
			#noRenderAxis:				(isError=true;	"Please select at least one projection in the Projection group.")
			#noRenderTexture:			(isError=true;	"Please select at least one texture in the Textures group.")
			#projectionComplete:		(isError=false;	"Projection render complete!")
			#projectionCancelled:		(isError=false;	"Projection render cancelled!")
			default:					(isError=true;	"Unknown error!")
		)
	),
	fn mBox messageCode title: debugExtraTxt: =
	(
		local beep
		messageBox (asobo_planeSeatProjStruct.getErrorMessage messageCode &title &beep defaultTitle:"Something went wrong..." debugExtraTxt:debugExtraTxt) title:title beep:beep
	),
	fn qBox messageCode extraInfos: title: =
	(
		local beep
		local msg = (asobo_planeSeatProjStruct.getErrorMessage messageCode &title &beep defaultTitle:"Confirm you want to continue?")
		if extraInfos != unsupplied then msg = msg + "\n" + extraInfos
		msg += "\n\nPlease confirm to continue."
		queryBox msg title:title beep:beep
	),
	fn createProgressBar =
	(
		rollout progress "Rendering projection maps" width:300 height:60
		(
			label lbProgress "Initialisation..."
			progressbar progBar height:24 color:(color 126 171 106)--(color 226 154 14)
		)
		createDialog progress
		progress.progBar.value = 0
		progress
	),
	fn updateProgressBar progressDialog barValue text: pauseOnUpdate:false =
	(
		progressDialog.progBar.value = barValue * 100.0
		if text != unsupplied then progressDialog.lbProgress.text = text
		if pauseOnUpdate then sleep 0.3
	),
	fn deleteProgressBar progressDialog =
	(
		destroyDialog progressDialog
	),
	
	/* NAMING */
	fn getName n allToLower:false firstToLower:false =
	(
		local t = case n of
			(
				#temp:				"ShouldBeDeleted"
				#altTemp:			"WorkingCopy"
				#normalMap:			"Normal"
				#heightMap:			"Height"
				#aoMap:				"AO"
				#emissiveMap:		"Emissive"
				#albedoMap:			"Albedo"
				#normalAoMap:		"Normal_ao"
				#albedoHeightMap:	"Albedo_height"
-- 				#normalHeightMap:	"Normal_height"
-- 				#albedoAoMap:		"Albedo_ao"
-- 				#heightAoMap:		"Height_ao"
				
				#top:		"top"
				#back:		"back"
				#front:		"front"
				#side:		"side"
				#topPlane:		"topPlane"
				#backPlane:		"backPlane"
				#frontPlane:	"frontPlane"
				#sidePlane:		"sidePlane"
				#projTopPlane:		"projection topPlane"
				#projBackPlane:		"projection backPlane"
				#projFrontPlane:	"projection frontPlane"
				#projSidePlane:		"projection sidePlane"
				#oppositeProjTopPlane:		"projection topBackPlane"
				#oppositeProjBackPlane:		"projection backBackPlane"
				#oppositeProjFrontPlane:	"projection frontBackPlane"
				#oppositeProjSidePlane:		"projection sideBackPlane"
				#projTopCamera:		"projection topCamera"
				#projBackCamera:	"projection backCamera"
				#projFrontCamera:	"projection frontCamera"
				#projSideCamera:	"projection sideCamera"
			)
		if allToLower then t = toLower t
		else if firstToLower then t = (toLower t[1]) + (substring t 2 -1)
		t
	),
	
	/* FILE OUTPUT */
	tiffSaveOptions = struct tiffSaveOptions
	(
		type,
		showControl,
		compression,
		alpha,
		dpi,
		fn setupDefaults =
		(
			this.type = #color
			this.showControl = #true
			this.compression = #none
			this.alpha = #true
			this.dpi = 300.0
		),
		on create do this.setupDefaults()
	);,
	tgaSaveOptions = struct tgaSaveOptions
	(
		colorDepth,
		compressed,
		alphaSplit,
		preMultAlpha,
		author,
		jobName,
		comment1,
		comment2,
		comment3,
		comment4,
		fn setupDefaults =
		(
			this.colorDepth = 32
			this.compressed = true
			this.alphaSplit = false
			this.preMultAlpha = false
			this.author = "Asobo"
			this.jobName = ""
			this.comment1 = ""
			this.comment2 = ""
			this.comment3 = ""
			this.comment4 = ""
		),
		on create do this.setupDefaults()
	);,
	pngSaveOptions = struct pngSaveOptions
	(
		type,
		alpha,
		interlaced,
		fn setupDefaults =
		(
			this.type = #true24
			this.alpha = true
			this.interlaced = false
		),
		on create do this.setupDefaults()
	);,
	bitmapSaveOptions = struct bitmapSaveOptions
	(
		tiff = (asobo_planeSeatProjStruct()).tiffSaveOptions(),
		tga = (asobo_planeSeatProjStruct()).tgaSaveOptions(),
		png = (asobo_planeSeatProjStruct()).pngSaveOptions()
	);,
	fn getSaveBitmapOptions =
	(
		local saveOptions = (asobo_planeSeatProjStruct()).bitmapSaveOptions()
		saveOptions.tiff.type			= TIF.getType			()
		saveOptions.tiff.showControl	= TIF.getShowControl	()
		saveOptions.tiff.compression	= TIF.getCompression	()
		saveOptions.tiff.alpha			= TIF.getAlpha			()
		saveOptions.tiff.dpi			= TIF.getDPI			()
		
		saveOptions.tga.colorDepth		= Targa.getColorDepth	()
		saveOptions.tga.compressed		= Targa.getCompressed	()
		saveOptions.tga.alphaSplit		= Targa.getAlphaSplit	()
		saveOptions.tga.preMultAlpha	= Targa.getPreMultAlpha	()
		saveOptions.tga.author			= Targa.getAuthor		()
		saveOptions.tga.jobName			= Targa.getJobName		()
		saveOptions.tga.comment1		= Targa.getComment1		()
		saveOptions.tga.comment2		= Targa.getComment2		()
		saveOptions.tga.comment3		= Targa.getComment3		()
		saveOptions.tga.comment4		= Targa.getComment4		()
		
		saveOptions.png.type			= pngio.getType			()
		saveOptions.png.alpha			= pngio.getAlpha		()
		saveOptions.png.interlaced		= pngio.getInterlaced	()
		
		saveOptions
	),
	fn compareSaveBitmapOptions saveOptions optSaveOptions: type:#tga =
	(
		if optSaveOptions == unsupplied then optSaveOptions = asobo_planeSeatProjStruct.getSaveBitmapOptions()
		if type == #tif then type = #tiff
		case type of
		(
			#tiff:		((saveOptions.tiff as string) == (optSaveOptions.tiff as string))
			#tga:		((saveOptions.tga as string) == (optSaveOptions.tga as string))
			#png:		((saveOptions.png as string) == (optSaveOptions.png as string))
			default:	false
		)
	),
	fn setupSaveBitmapOptions saveOptions: type: =
	(
		local success = true
		if saveOptions == unsupplied then saveOptions = (asobo_planeSeatProjStruct()).bitmapSaveOptions()
		case of
		(
			(type == #all or type == #tif or type == #tiff):
			(
				TIF.setType				(saveOptions.tiff.type)
				TIF.setShowControl		(saveOptions.tiff.showControl)
				TIF.setCompression		(saveOptions.tiff.compression)
				TIF.setAlpha			(saveOptions.tiff.alpha)
				TIF.setDPI				(saveOptions.tiff.dpi)
			)
			(type == #all or type == #tga):
			(
				Targa.setColorDepth		(saveOptions.tga.colorDepth)
				Targa.setCompressed		(saveOptions.tga.compressed)
				Targa.setAlphaSplit		(saveOptions.tga.alphaSplit)
				Targa.setPreMultAlpha	(saveOptions.tga.preMultAlpha)
				Targa.setAuthor			(saveOptions.tga.author)
				Targa.setJobName		(saveOptions.tga.jobName)
				Targa.setComment1		(saveOptions.tga.comment1)
				Targa.setComment2		(saveOptions.tga.comment2)
				Targa.setComment3		(saveOptions.tga.comment3)
				Targa.setComment4		(saveOptions.tga.comment4)
			)
			(type == #all or type == #png):
			(
				pngio.setType			(saveOptions.png.type)
				pngio.setAlpha			(saveOptions.png.alpha)
				pngio.setInterlaced		(saveOptions.png.interlaced)
			)
			default:
			(
				success = false
			)
		)
		success
	),
	fn setupMinimumSafeSaveBitmapOptions saveOptions: type: =
	(
		local success = true
		if saveOptions == unsupplied then saveOptions = (asobo_planeSeatProjStruct()).bitmapSaveOptions()
		case type of
		(
			#tiff:
			(
				saveOptions.tiff.alpha = #true
			)
			#tga:
			(
				saveOptions.tga.colorDepth = 32
				saveOptions.tga.compressed = true
				saveOptions.tga.alphaSplit = false
				--saveOptions.tga.preMultAlpha = false
			)
			default:
			(
				success = false
			)
		)
		success
	),
	textureFilenames = struct textureFilenames
	(
		normalMap,
		heightMap,
		aoMap,
		emissiveMap,
		albedoMap
	);,
	combinedTextureFilenames = struct combinedTextureFilenames
	(
-- 		heightAoMap
-- 		normalHeightMap,
-- 		albedoAoMap,
		normalAoMap,
		albedoHeightMap
	);,
	fn getTextureArrayFolder fileName suffix: =
	(
		local f = fileName
		if suffix != unsupplied then f = f + "_" + suffix
		f + ".textureArray\\"
	),
	fn createFilename fileName fileExtension type suffix: temp:false altTemp:false useTextureArrayFolder:true =
	(
		local f = fileName
		if temp then f = (asobo_planeSeatProjStruct.getName (if altTemp then #altTemp else #temp) firstToLower:true) + "_" + f
		if useTextureArrayFolder then f = (asobo_planeSeatProjStruct.getTextureArrayFolder fileName suffix:suffix) + f
		if suffix != unsupplied then f = f + "_" + suffix
		f + "_" + (asobo_planeSeatProjStruct.getName type allToLower:true) + fileExtension
	),
	fn getAxisFilenames texFilePath texFileName texFileExtension axisName renderInfos altTemp:false useTextureArrayFolder:true =
	(
		local pn = asobo_planeSeatProjStruct.getName axisName allToLower:true
		local texFilenames = (asobo_planeSeatProjStruct()).textureFilenames()
		if renderInfos.normal.active 	then texFilenames.normalMap =	texFilePath + (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #normalMap		suffix:pn	\
			temp:renderInfos.normal.temp	altTemp:altTemp	useTextureArrayFolder:useTextureArrayFolder)
		if renderInfos.height.active 	then texFilenames.heightMap =	texFilePath + (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #heightMap		suffix:pn	\
			temp:renderInfos.height.temp	altTemp:altTemp	useTextureArrayFolder:useTextureArrayFolder)
		if renderInfos.ao.active 		then texFilenames.aoMap =		texFilePath + (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #aoMap			suffix:pn	\
			temp:renderInfos.ao.temp		altTemp:altTemp	useTextureArrayFolder:useTextureArrayFolder)
		if renderInfos.emissive.active 	then texFilenames.emissiveMap =	texFilePath + (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #emissiveMap	suffix:pn	\
			temp:renderInfos.emissive.temp	altTemp:altTemp	useTextureArrayFolder:useTextureArrayFolder)
		if renderInfos.albedo.active 	then texFilenames.albedoMap =	texFilePath + (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #albedoMap		suffix:pn	\
			temp:renderInfos.albedo.temp	altTemp:altTemp	useTextureArrayFolder:useTextureArrayFolder)
		texFilenames
	),
	fn getAxisCombinedFilenames texFilePath texFileName texFileExtension axisName renderInfos useTextureArrayFolder:true =
	(
		local pn = asobo_planeSeatProjStruct.getName axisName allToLower:true
		local combinedTexFilenames = (asobo_planeSeatProjStruct()).combinedTextureFilenames()
-- 		if renderInfos.height.active	and renderInfos.ao.active 		then combinedTexFilenames.heightAoMap =		texFilePath + \
-- 			(asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #HeightAoMap		suffix:pn	useTextureArrayFolder:useTextureArrayFolder)
-- 		if renderInfos.normal.active	and renderInfos.height.active 	then combinedTexFilenames.normalHeightMap =	texFilePath + \
-- 			(asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #normalHeightMap	suffix:pn	useTextureArrayFolder:useTextureArrayFolder)
-- 		if renderInfos.albedo.active 	and renderInfos.ao.active		then combinedTexFilenames.albedoAoMap =		texFilePath + \
-- 			(asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #albedoAoMap		suffix:pn	useTextureArrayFolder:useTextureArrayFolder)
		if renderInfos.normal.active	and renderInfos.ao.active 		then combinedTexFilenames.normalAoMap =		texFilePath + \
			(asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #normalAoMap		suffix:pn	useTextureArrayFolder:useTextureArrayFolder)
		if renderInfos.albedo.active 	and renderInfos.height.active	then combinedTexFilenames.albedoHeightMap =	texFilePath + \
			(asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #albedoHeightMap	suffix:pn	useTextureArrayFolder:useTextureArrayFolder)
		combinedTexFilenames
	),
	-- for some reason maxscript fails when dealing with relative paths here.
	fn doesFileExistSafe filename =
	(
		doesFileExist (pathConfig.convertPathToAbsolute filename)
	),
	-- matchingFiles needs to be an array
	fn checkFileExists texFilenames &matchingFiles =
	(
		if texFilenames.normalMap != undefined		then if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.normalMap		then append matchingFiles (filenameFromPath texFilenames.normalMap)
		if texFilenames.heightMap != undefined		then if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.heightMap		then append matchingFiles (filenameFromPath texFilenames.heightMap)
		if texFilenames.aoMap != undefined			then if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.aoMap			then append matchingFiles (filenameFromPath texFilenames.aoMap)
		if texFilenames.emissiveMap != undefined	then if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.emissiveMap	then append matchingFiles (filenameFromPath texFilenames.emissiveMap)
		if texFilenames.albedoMap != undefined		then if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.albedoMap		then append matchingFiles (filenameFromPath texFilenames.albedoMap)
		matchingFiles.count != 0
	),
	fn checkCombinedFileExists combinedTexFilenames &matchingFiles =
	(
		if combinedTexFilenames.normalAoMap != undefined		then if asobo_planeSeatProjStruct.doesFileExistSafe combinedTexFilenames.normalAoMap		then append matchingFiles (filenameFromPath combinedTexFilenames.normalAoMap)
		if combinedTexFilenames.albedoHeightMap != undefined	then if asobo_planeSeatProjStruct.doesFileExistSafe combinedTexFilenames.albedoHeightMap	then append matchingFiles (filenameFromPath combinedTexFilenames.albedoHeightMap)
		matchingFiles.count != 0
	),
	fn addFilePathEndSlash path =
	(
		if path[ path.count ] != "\\" then
			path += "\\"
		path
	),
	fn removeFilePathEndSlash path =
	(
		if path[ path.count ] == "\\" then
			path = substring path 1 (path.count - 1)
		path
	),
	fn fixFilePath path =
	(
		pathConfig.resolvePathSymbols path
	),
	fn getAfterDotFilenameType filename =
	(
		local ext = getFilenameType filename
		if ext[1] == "." then
			ext = substring ext 2 ext.count
		ext
	),
	fn getAfterDotFilenameTypeName filename autoCorrect:true =
	(
		local ext = (asobo_planeSeatProjStruct.getAfterDotFilenameType filename) as name
		if autoCorrect then
		(
			if ext == #tif then ext = #tiff
		)
		ext
	),
	fn checkFileName filename =
	(
		getFilenameFile filename != "" and asobo_planeSeatProjStruct.getAfterDotFilenameType filename != ""
	),
	fn checkFilePath filename =
	(
		getFilenamePath filename != ""
	),
	fn getLastFolderName filename =
	(
		local f = getFilenamePath filename
		local folders = filterString f "\\/"
		folders[folders.count]
	),
	fn isFolderCreated filename =
	(
		if not doesDirectoryExist filename then makeDir filename all:false --all to false will only allow to create the last directory in the path, all other must already exists
		else true
	),
	fn getHistoryString nb =
	(
		"History_" + (formattedprint nb format:"02d")
	),
	fn getAllSaveHistory ini historyCategory =
	(
		local saveHistory = #()
		local highestSaveEntryFound = false
		local saveEntryCurrentNb = 0
		while not highestSaveEntryFound do
		(
			local currentHistoryString = asobo_planeSeatProjStruct.getHistoryString saveEntryCurrentNb
			if hasINISetting ini historyCategory currentHistoryString then
			(
				saveHistory[saveEntryCurrentNb + 1] = getINISetting ini historyCategory currentHistoryString
				saveEntryCurrentNb += 1
			)
			else highestSaveEntryFound = true
		)
		saveHistory
	),
	fn manageSaveHistory mode:#get setPath: =
	(
		-- try to replicate default history behavior for bitmap dialog
		-- note: if no history yet, #get will return ""
		local historyCategory = "planeSeatProj"
		local maxHistoryCount = 3
		
		local currentHistoryCount = 0
		local lastpath = ""
		local maxINI = getMAXIniFile()
		if not hasINISetting maxINI historyCategory then
		(
			setINISetting maxINI historyCategory "Count" "0"
		)
		else
		(
			currentHistoryCount = (getINISetting maxINI historyCategory "Count") as integer
		)
		
		if currentHistoryCount > 0 then lastpath = getINISetting maxINI historyCategory (asobo_planeSeatProjStruct.getHistoryString 0)
		case mode of
		(
			#get:
			(
				lastPath
			)
			#set:
			(
				-- note: history entries are 0 based
				if lastpath != setPath then
				(
					local allEntries = asobo_planeSeatProjStruct.getAllSaveHistory maxINI historyCategory
					local duplicateEntryID = findItem allEntries setPath
					local shiftStart = if duplicateEntryID != 0 then duplicateEntryID - 1 else maxHistoryCount
					-- shift entries
					for i = shiftStart to 1 by -1 do
					(
						local currentHistoryString = asobo_planeSeatProjStruct.getHistoryString (i-1)
						if hasINISetting maxINI historyCategory currentHistoryString then
						(
							local previousPathEntry = getINISetting maxINI historyCategory currentHistoryString
							setINISetting maxINI historyCategory (asobo_planeSeatProjStruct.getHistoryString i) previousPathEntry
						)
					)
					-- save last
					setINISetting maxINI historyCategory (asobo_planeSeatProjStruct.getHistoryString 0) setPath
					if duplicateEntryID == 0 then currentHistoryCount += 1
				)
				-- remove older entries (this will also handle entries if maxHistoryCount is changed)
				if currentHistoryCount > maxHistoryCount then
				(
					local highestSaveEntryFound = false
					local saveEntryCurrentNb = maxHistoryCount
					while not highestSaveEntryFound do
					(
						local currentHistoryString = asobo_planeSeatProjStruct.getHistoryString saveEntryCurrentNb
						if hasINISetting maxINI historyCategory currentHistoryString then
						(
							delIniSetting maxINI historyCategory currentHistoryString
						)
						else highestSaveEntryFound = true
					)
					currentHistoryCount = maxHistoryCount
				)
				setINISetting maxINI historyCategory "Count" (currentHistoryCount as string)
			)
		)
	),
	fn getSaveHistory =
	(
		local path = asobo_planeSeatProjStruct.manageSaveHistory mode:#get
		path = asobo_planeSeatProjStruct.addFilePathEndSlash path
		path
	),
	fn setSaveHistory lastPath =
	(
		lastPath = asobo_planeSeatProjStruct.removeFilePathEndSlash (asobo_planeSeatProjStruct.fixFilePath lastPath)
		asobo_planeSeatProjStruct.manageSaveHistory mode:#set setPath:lastPath
	),
	fn checkFileFormat filename =
	(
		local fileExtension = asobo_planeSeatProjStruct.getAfterDotFilenameTypeName filename
		local success = case fileExtension of
		(
			#tiff:		true
			#tga:		false
			#png:		false
			default:	false
		)
		if not success then asobo_planeSeatProjStruct.mBox #unsupportedFileFormat debugExtraTxt:(fileExtension as string)
		success
	),
	-- proper save bitmap dialog: allow to set proper options depending on file format
	-- turns out we DONT WANT user to be able to set custom parameters and this dialog doesn't allow for file format control
	fn chooseSaveBitmap &fallbackToForced filename: =
	(
		local gamma, bitmapSaveMetaData
		local f = selectSaveBitMap \
			caption:"Save bitmap as" \
			filename:filename
		if f != undefined then
		(
			if asobo_planeSeatProjStruct.checkFileFormat f then
			(
				fallbackToForced = false
				asobo_planeSeatProjStruct.setSaveHistory (getFilenamePath f)
			)
			else
			(
				fallbackToForced = true
				f = asobo_planeSeatProjStruct.chooseSavePath filename:filename --revert to more controlled environment if user dont choose properly
			)
		)
		f
	),
	fn getSavetypes type =
	(
		if type == #tif then type = #tiff
		case type of
		(
			#tiff:		"Tiff Image File (*.tif)|*.tif"
			#tga:		"Targa Image File (*.tga)|*.tga"
			#bmp:		"Bitmap Image File (*.bmp)|*.bmp"
			#png:		"PNG Image File (*.png)|*.png"
			default:	"Tiff Image File (*.tif)|*.tif" -- default or #all
		)
	),
	fn chooseSavePath type:#all filename: =
	(
		local f = getSaveFileName \
			caption:"Save bitmap as" \
			filename:(if filename != unsupplied then filename else "") \
			types:(asobo_planeSeatProjStruct.getSavetypes type) \
			historyCategory:"planeSeatProj"
		if f != undefined then
		(
			if not asobo_planeSeatProjStruct.checkFileFormat f then f = asobo_planeSeatProjStruct.chooseSavePath filename:filename
		)
		f
	),
	fn deleteAxisTempFiles axisFilenames tempTextures =
	(
		for tex in getPropNames tempTextures do
		(
			if (getProperty tempTextures tex) then
			(
				local tempFilename = getProperty axisFilenames tex
				deleteFile tempFilename
			)
		)
	),
	
	/* SANITIZE SELECTION */
	fn isObjectValidForRenderToTexture o =
	(
		(IsValidNode o) and (superClassOf o == GeometryClass)
	),
	fn filterObjects objArray =
	(
		newArray = copy objArray #nomap
		for i = newArray.count to 1 by -1 do
		(
			if not asobo_planeSeatProjStruct.isObjectValidForRenderToTexture newArray[i] then deleteItem newArray i
		)
		newArray
	),
	
	/* MATH */
	fn roundNb nbToRound afterComma:0 =
	(
		floor ( ((pow 10 afterComma) * nbToRound + 0.5) ) / (pow 10 afterComma)
	),
	fn upMultiple nbToUp multiple:4 =
	(
		multiple = multiple as float
		nbToUp = nbToUp as float
		(ceil (nbToUp/multiple)) * multiple
	),
	
	/* 3D */
	fn getMaxVectorAxis inputvector =
	(
		local axis
		if inputVector.x < inputVector.y then
		(
			if inputVector.y < inputVector.z then axis = #Z
			else axis = #Y
		)
		else
		(
			if inputVector.x < inputVector.z then axis = #Z
			else axis = #X
		)
		axis
	),
	fn floorVector inputVector =
	(
		[floor inputVector.x, floor inputVector.y, floor inputVector.z]
	),
	fn intVector inputVector =
	(
		[inputVector.x as integer, inputVector.y as integer, inputVector.z as integer]
	),
	fn absVector inputVector =
	(
		[abs inputVector.x, abs inputVector.y, abs inputVector.z]
	),
	fn maxVector inputVector maxValue =
	(
		[amax inputVector.x maxValue, amax inputVector.y maxValue, amax inputVector.z maxValue]
	),
	fn upMultipleVector inputVector multiple:4 =
	(
		[asobo_planeSeatProjStruct.upMultiple inputVector.x multiple:multiple, asobo_planeSeatProjStruct.upMultiple inputVector.y multiple:multiple, asobo_planeSeatProjStruct.upMultiple inputVector.z multiple:multiple]
	),
	fn getBBox obj =
	(
		nodeGetBoundingBox obj (matrix3 1)
	),
	fn safeBBox bBox amount =
	(
		#((bBox[1]-amount), (bBox[2]+amount))
	),
	fn expandBBox obj &bBox =
	(
		local newBBox = asobo_planeSeatProjStruct.getBBox obj
		bBox = #(	[amin newBBox[1].x bBox[1].x, amin newBBox[1].y bBox[1].y, amin newBBox[1].z bBox[1].z],
					[amax newBBox[2].x bBox[2].x, amax newBBox[2].y bBox[2].y, amax newBBox[2].z bBox[2].z])
	),
	fn getSelectionBB objArray =
	(
		-- require objArray.count > 0
		local bb = asobo_planeSeatProjStruct.getBBox objArray[1]
		for i = 2 to objArray.count do expandBBox objArray[i] &bb
		bb
	),
	fn getBBoxCenter bBox =
	(
		(bBox[2] + bBox[1]) / 2.0
	),
	fn getBBoxSize bBox =
	(
		asobo_planeSeatProjStruct.absVector (bBox[1] - bBox[2])
	),
	boundingBox = struct boundingBox
	(
		bBox,
		bbMin,
		bbMax,
		bbCenter,
		bbSize,
		fn bbSet bBox =
		(
			this.bbMin = bBox[1]
			this.bbMax = bBox[2]
			this.bbCenter = asobo_planeSeatProjStruct.getBBoxCenter bBox
			this.bbSize = asobo_planeSeatProjStruct.getBBoxSize bBox
		),
		on create do
		(
			if this.bBox != undefined then
			(
				this.bbMin = this.bBox[1]
				this.bbMax = this.bBox[2]
				this.bbCenter = asobo_planeSeatProjStruct.getBBoxCenter this.bBox
				this.bbSize = asobo_planeSeatProjStruct.getBBoxSize this.bBox
			)
		)
	);,
	fn getRotationToAxisVec axis =
	(
		case axis of
		(
			#plusX:		[90, 0, 90]
			#plusY:		[90, 0, 0]
			#plusZ:		[0, 0, 0]
			#minusX:	[90, 0, -90]
			#minusY:	[90, 0, 180]
			#minusZ:	[0, 180, 0]
		)
	),
	fn setObjectRotation o vec =
	(
		o.rotation.controller.X_Rotation = vec.x
		o.rotation.controller.Y_Rotation = vec.y
		o.rotation.controller.Z_Rotation = vec.z
	),
	fn objectRotationToAxis o axis =
	(
		asobo_planeSeatProjStruct.setObjectRotation o (asobo_planeSeatProjStruct.getRotationToAxisVec axis)
	),
	
	/* PRE RENDER */
	projectionObjectsPerAxis = struct projectionObjectsPerAxis
	(
		top,
		back,
		front,
		side
	);,
	projectionObjects = struct projectionObjects
	(
		normal,
		height,
		ao,
		emissive,
		albedo
	);,
	fn createRenderObjects objsToRender bBox renderInfos &progressDialog layer: =
	(
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (0.0) text:"Projection setup (please wait even if 3dsmax seems to freeze)"
		
		local renderObjs = (asobo_planeSeatProjStruct()).projectionObjects()
		
		-- lets speed things up by avoiding to create material duplicates
		local materialsUsed = #()
		local materialCorrespondance = #()
		materialCorrespondance[objsToRender.count] = undefined --init size
		for i = 1 to objsToRender.count do
		(
			local matchingMatID = findItem materialsUsed objsToRender[i].material
			if matchingMatID == 0 then
			(
				append materialsUsed objsToRender[i].material
				materialCorrespondance[i] = materialsUsed.count
			)
			else
			(
				materialCorrespondance[i] = matchingMatID
			)
		)
		local newMaterials = (asobo_planeSeatProjStruct()).projectionObjects normal:#() height:((asobo_planeSeatProjStruct()).projectionObjectsPerAxis top:#() back:#() front:#() side:#()) ao:#() emissive:#() albedo:#()
		newMaterials.normal[materialsUsed.count] = undefined --init size
		newMaterials.height.top[materialsUsed.count] = undefined --init size
		newMaterials.height.back[materialsUsed.count] = undefined --init size
		newMaterials.height.front[materialsUsed.count] = undefined --init size
		newMaterials.height.side[materialsUsed.count] = undefined --init size
		newMaterials.ao[materialsUsed.count] = undefined --init size
		newMaterials.emissive[materialsUsed.count] = undefined --init size
		newMaterials.albedo[materialsUsed.count] = undefined --init size
		
		-- duplicate objects if needed
		if renderInfos.normal.active	then
		(
			if renderInfos.normal.renderType == #projection and renderInfos.normal.projectionType == #default then renderObjs.normal = objsToRender --can reuse input here
				else renderObjs.normal = for o in objsToRender collect copy o
		)
		if renderInfos.height.active	then
		(
			if renderInfos.height.renderType == #projection and renderInfos.height.projectionType == #default then renderObjs.height = objsToRender --can reuse input here
			else
			(
				renderObjs.height = (asobo_planeSeatProjStruct()).projectionObjectsPerAxis()
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	renderObjs.height.top = for o in objsToRender collect copy o
						#back:	renderObjs.height.back = for o in objsToRender collect copy o
						#front:	renderObjs.height.front = for o in objsToRender collect copy o
						#side:	renderObjs.height.side = for o in objsToRender collect copy o
					)
				)
			)
		)
		if renderInfos.ao.active		then
		(
			if renderInfos.ao.renderType == #projection and renderInfos.ao.projectionType == #default then renderObjs.ao = objsToRender --can reuse input here
				else renderObjs.ao = for o in objsToRender collect copy o
		)
		if renderInfos.emissive.active	then renderObjs.emissive = for o in objsToRender collect copy o
		if renderInfos.albedo.active	then renderObjs.albedo = for o in objsToRender collect copy o
		
		-- keep scene organized
		if layer != unsupplied then
		(
			if renderInfos.normal.active	and not (renderInfos.normal.renderType == #projection and renderInfos.normal.projectionType == #default)	then for o in renderObjs.normal		do layer.addNode o
			if renderInfos.height.active	and not (renderInfos.height.renderType == #projection and renderInfos.height.projectionType == #default)	then
			(
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	for o in renderObjs.height.top		do layer.addNode o
						#back:	for o in renderObjs.height.back		do layer.addNode o
						#front:	for o in renderObjs.height.front	do layer.addNode o
						#side:	for o in renderObjs.height.side		do layer.addNode o
					)
				)
			)
			if renderInfos.ao.active		and not (renderInfos.ao.renderType == #projection and renderInfos.ao.projectionType == #default)	then for o in renderObjs.ao			do layer.addNode o
			if renderInfos.emissive.active	then for o in renderObjs.emissive	do layer.addNode o
			if renderInfos.albedo.active	then for o in renderObjs.albedo		do layer.addNode o
		)
		--just for debugging
		if renderInfos.normal.active	and not (renderInfos.normal.renderType == #projection and renderInfos.normal.projectionType == #default)	then for i = 1 to objsToRender.count do renderObjs.normal[i].name = "normal_" + objsToRender[i].name
		if renderInfos.height.active	and not (renderInfos.height.renderType == #projection and renderInfos.height.projectionType == #default)	then
		(
			for renderAxis in renderInfos.renderAxis do
			(
				case renderAxis of
				(
					#top:	for i = 1 to objsToRender.count do renderObjs.height.top[i].name = "height_top_" + objsToRender[i].name
					#back:	for i = 1 to objsToRender.count do renderObjs.height.back[i].name = "height_back_" + objsToRender[i].name
					#front:	for i = 1 to objsToRender.count do renderObjs.height.front[i].name = "height_front_" + objsToRender[i].name
					#side:	for i = 1 to objsToRender.count do renderObjs.height.side[i].name = "height_side_" + objsToRender[i].name
				)
			)
		)
		if renderInfos.ao.active		and not (renderInfos.ao.renderType == #projection and renderInfos.ao.projectionType == #default)	then for i = 1 to objsToRender.count do renderObjs.ao[i].name = "ao_" + objsToRender[i].name
		if renderInfos.emissive.active	then for i = 1 to objsToRender.count do renderObjs.emissive[i].name = "emissive_" + objsToRender[i].name
		if renderInfos.albedo.active	then for i = 1 to objsToRender.count do renderObjs.albedo[i].name = "albedo_" + objsToRender[i].name
		
		-- create custom materials if needed
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (1.0 / 6.0)
		if renderInfos.normal.active	and not (renderInfos.normal.renderType == #projection and renderInfos.normal.projectionType == #default)	then
		(
			for i = 1 to renderObjs.normal.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.normal[i]	&newMaterials.normal[materialCorrespondance[i]] map:#normalMap	rendererType:renderInfos.normal.rendererType
		)
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (2.0 / 6.0)
		if renderInfos.height.active	and not (renderInfos.height.renderType == #projection and renderInfos.height.projectionType == #default)	then
		(
			for renderAxis in renderInfos.renderAxis do
			(
				case renderAxis of
				(
					#top:	for i = 1 to renderObjs.height.top.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.height.top[i]	&newMaterials.height.top[materialCorrespondance[i]]		map:#heightMap	rendererType:renderInfos.height.rendererType	heightMapAxis:#Z	heightMapRange:[bBox.bbMin.z,bBox.bbMax.z]
					#back:	for i = 1 to renderObjs.height.back.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.height.back[i]	&newMaterials.height.back[materialCorrespondance[i]]	map:#heightMap	rendererType:renderInfos.height.rendererType	heightMapAxis:#Y	heightMapRange:[bBox.bbMin.y,bBox.bbMax.y]
					#front:	for i = 1 to renderObjs.height.front.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.height.front[i]	&newMaterials.height.front[materialCorrespondance[i]]	map:#heightMap	rendererType:renderInfos.height.rendererType	heightMapAxis:#Y	heightMapRange:[bBox.bbMax.y,bBox.bbMin.y]
					#side:	for i = 1 to renderObjs.height.side.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.height.side[i]	&newMaterials.height.side[materialCorrespondance[i]]	map:#heightMap	rendererType:renderInfos.height.rendererType	heightMapAxis:#X	heightMapRange:[bBox.bbMax.x,bBox.bbMin.x]
				)
			)
		)
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (3.0 / 6.0)
		if renderInfos.ao.active		and not (renderInfos.ao.renderType == #projection and renderInfos.ao.projectionType == #default)	then
		(
			for i = 1 to renderObjs.ao.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.ao[i] &newMaterials.ao[materialCorrespondance[i]] map:#aoMap		rendererType:renderInfos.ao.rendererType
		)
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (4.0 / 6.0)
		if renderInfos.emissive.active	then for i = 1 to renderObjs.emissive.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.emissive[i]	&newMaterials.emissive[materialCorrespondance[i]] map:#emissiveMap	rendererType:renderInfos.emissive.rendererType
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (5.0 / 6.0)
		if renderInfos.albedo.active	then for i = 1 to renderObjs.albedo.count	do asobo_planeSeatProjStruct.convertNodeMaterialToRenderMaterial renderObjs.albedo[i]	&newMaterials.albedo[materialCorrespondance[i]] map:#albedoMap	rendererType:renderInfos.albedo.rendererType
		asobo_planeSeatProjStruct.updateProgressBar progressDialog (6.0 / 6.0) pauseOnUpdate:true
		
		renderObjs
	),
	
	/* GEOMETRY */
	projectionPlanes = struct projectionPlanes
	(
		normal,
		height,
		ao,
		emissive,
		albedo
	);,
	projectionPlane = struct projectionPlane
	(
		projPlane,
		texSize,
		bugFixTexSize,
		zSize,
		texFilenames,
		projMod,
		rendererType
	);,
	projectionBackPlanes = struct projectionBackPlanes
	(
		normal,
		height
	);,
	fn createPlane pos axis size texSize bugFixTexSize texFilenames rendererType name: layer: =
	(
		local newPlane = Plane name:name position:pos length:size.y width:size.x lengthsegs:1 widthsegs:1 density:1 renderScale:1 mapCoords:true realWorldMapSize:false
		asobo_planeSeatProjStruct.objectRotationToAxis newPlane axis
		if layer != unsupplied then layer.addNode newPlane
		newPlane.xray = true
		newPlane.backfaceCull = true
		(asobo_planeSeatProjStruct()).projectionPlane projPlane:newPlane texSize:texSize bugFixTexSize:bugFixTexSize zSize:size.z texFilenames:texFilenames rendererType:rendererType
	),
	fn createProjectionPlane pos axis size texSize bugFixTexSize texFilenames projObjs rendererType name: layer: =
	(
		local newPlane = asobo_planeSeatProjStruct.createPlane pos axis size texSize bugFixTexSize texFilenames rendererType name:name layer:layer
		local newProjMod = Projection()
		addModifier newPlane.projPlane newProjMod
		newPlane.projMod = newProjMod
		for o in projObjs do newProjMod.projectionModOps.addObjectNode o
		newPlane
	),
	fn createProjectionPlanes pos axis size texSize bugFixTexSize texFilenames projObjs backPlanes renderInfos name: layer: =
	(
		local renderPlanes = (asobo_planeSeatProjStruct()).projectionPlanes()
		if renderInfos.normal.active	and renderInfos.normal.renderType == #projection		then renderPlanes.normal = asobo_planeSeatProjStruct.createProjectionPlane pos axis size texSize bugFixTexSize texFilenames (projObjs.normal+#(backPlanes.normal)) renderInfos.normal.rendererType name:(name + "_normal") layer:layer
		if renderInfos.height.active	and renderInfos.height.renderType == #projection		then renderPlanes.height = asobo_planeSeatProjStruct.createProjectionPlane pos axis size texSize bugFixTexSize texFilenames (projObjs.height+#(backPlanes.height)) renderInfos.height.rendererType name:(name + "_height") layer:layer
		if renderInfos.ao.active		and renderInfos.ao.renderType == #projection			then renderPlanes.ao = asobo_planeSeatProjStruct.createProjectionPlane pos axis size texSize bugFixTexSize texFilenames projObjs.ao renderInfos.ao.rendererType name:(name + "_ao") layer:layer
		if renderInfos.emissive.active	and renderInfos.emissive.renderType == #projection		then renderPlanes.emissive = asobo_planeSeatProjStruct.createProjectionPlane pos axis size texSize bugFixTexSize texFilenames projObjs.emissive renderInfos.emissive.rendererType name:(name + "_emissive") layer:layer
		if renderInfos.albedo.active	and renderInfos.albedo.renderType == #projection		then renderPlanes.albedo = asobo_planeSeatProjStruct.createProjectionPlane pos axis size texSize bugFixTexSize texFilenames projObjs.albedo renderInfos.albedo.rendererType name:(name + "_albedo") layer:layer
		renderPlanes
	),
	fn createProjectionBackPlane pos axis size name: layer: =
	(
		local newPlane = Plane name:name position:pos length:size.y width:size.x lengthsegs:1 widthsegs:1 density:1 renderScale:1 mapCoords:true realWorldMapSize:false
		asobo_planeSeatProjStruct.objectRotationToAxis newPlane axis
		if layer != unsupplied then layer.addNode newPlane
		newPlane.xray = true
		newPlane.backfaceCull = true
		newPlane
	),
	fn createProjectionBackPlanes pos axis size renderInfos name: layer: =
	(
		local renderBackPlanes = (asobo_planeSeatProjStruct()).projectionBackPlanes()
		if renderInfos.normal.active then
		(
			renderBackPlanes.normal = asobo_planeSeatProjStruct.createProjectionBackPlane pos axis size name:(name + "_normal") layer:layer
			renderBackPlanes.normal.material = asobo_planeSeatProjStruct.createDebugRenderMaterial map:#normalMap rendererType:renderInfos.normal.rendererType invertNormal:true --invert normal as auto "bleed"
		)
		if renderInfos.height.active then
		(
			renderBackPlanes.height = asobo_planeSeatProjStruct.createProjectionBackPlane pos axis size name:(name + "_height") layer:layer
			renderBackPlanes.height.material = asobo_planeSeatProjStruct.createDebugRenderMaterial map:#albedoMap albedoColor:black rendererType:renderInfos.height.rendererType
		)
		renderBackPlanes
	),
	
	/* LAYERS */
	fn createLayer layerName:"Objects projection" setVisible:true =
	(
		local newLayer = layerManager.getLayerFromName layerName
		if newLayer == undefined then
		(
			newLayer = layerManager.newLayer()
			newLayer.setName layerName
		)
		newLayer.on = false
		newLayer.ishidden = not setVisible
		newLayer
	),
	fn deleteLayer layer =
	(
		layerManager.deleteLayerByName layer.name
	),
	
	/* MATERIAL */
	-- debug material displays a purple checker
	fn createDebugMap =
	(
		local debugMap = checker Color1:(color 58 13 113) Color2:(color 143 51 230)
		debugMap.coordinates.uTiling = debugMap.coordinates.vTiling = 4
		debugMap
	),
	--OSL nodes
	fn matFloatNode =
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/SetFloat.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode
	),
	fn matFloatClampNode =
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/FloatClamp.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode
	),
	fn matMultiplyNode =
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/ColorMul.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode
	),
	fn matAddNode =
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/VectorAdd.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode
	),
	fn matLerpNode =
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/Interpolate.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode
	),
	fn matColorNode =
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/SetColor.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode
	),
	fn matCoordNode coordSpace:#world = --world|object|camera|shader|screen|3dsmaxscreen|NDC|raster
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/GetCoordSpace.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode.Coordspace = coordSpace as string
		matNode
	),
	fn matNormalNode coordSpace:#world = --world|object|camera|shader|screen|NDC|raster
	(
		local OSLShaderFilename = (getdir #maxroot) + "OSL/Normal.osl"
		local matNode = OSLMap()
		matNode.OSLPath = OSLShaderFilename
		matNode.Coordspace = coordSpace as string
		matNode
	),
	fn matNormalFinalTweak invertNormal:false =
	(
		local matNode = OSLMap()
		matNode.OSLCode = "shader NormalFSTweak
(
	color NormalMap = 1.0 [[ string label = \"NormalMap\" ]],
	int InvertNormal = 0 [[ string widget=\"checkBox\", string label = \"Invert Normal\" ]],
	output color Out = 0.0,
)
{
	vector t = NormalMap * 2.0 - 1.0;
	t = vector(-t.x, t.z, -t.y);//Felt more comfortable having x that way by default :)
	if(InvertNormal) t *= -1;
	t = t * 0.5 + 0.5;
	
	Out = t;
}"
		matNode.InvertNormal = invertNormal
		matNode
	),
	fn matNormalTangentToWorldNode =
	(
		local matNode = OSLMap()
		matNode.OSLCode = "void make_orthonormals(vector N, output vector a, output vector b)
{
  a = cross(vector(0, 0, 1), N);
  if(length(a) == 0.0)
  {
  	float dirDot = dot(vector(0,0,1), N);
  	a = vector(dirDot, 0.0, 0.0);
  }
  a = normalize(a);
  b = cross(N, a);
}

shader NormalMapToWorld
(
	color NormalMap = 1.0 [[ string label = \"NormalMap\" ]],
	output color Out = 0.0,
)
{
	vector T, B;
	make_orthonormals(N, T, B);
	
	matrix m = matrix (	T.x, B.x, N.x, 0.0,
						T.y, B.y, N.y, 0.0,
						T.z, B.z, N.z, 0.0,
						0.0, 0.0, 0.0, 1.0);
	m = transpose(m);
	
	vector t = transform(m, normalize(NormalMap));
	t = t * 0.5 + 0.5;
	
	Out = t;
}"
		matNode
	),
	fn matAONode =
	(
		local matNode = OSLMap()
		matNode.OSLCode = "// Converted existing OSL shader for 3dsmax...

/*
 * BaAmbientOcclusion.osl by Bao2 (c)2012
 * from https://github.com/sambler/osl-shaders
 *
 * original script from -
 * http://blenderartists.org/forum/showthread.php?270332-OSL-Goodness/page10
 *
 */

/* Original code from Brecht:
   http://projects.blender.org/scm/viewvc.php?view=rev&root=bf-blender&revision=51952

   Mode: 0: Concave (AO)
         1: Convex (Wear)
         2: Both

   InvertEffect: Swaps Effect and No_Effect colors

   Samples: 1 or above (set 0 or negative to turn off the effect)

   Output Color: Mix between the two colors driven by Fac
   Output Fac: Exposed because it can be useful to have it too
*/

void rng_seed(output int rng, int seed)
{
  int chash = seed;
  if (chash == 0) chash = 1;
  rng = chash * 891694213;
}

float rng_uniform(output int rng)
{
  float res = rng / float(2137483647) * 0.5 + 0.5;
  rng *= 891694213;
  return res;
}

void to_unit_disk(float x, float y, output float x_out, output float y_out)
{
  float r, phi;
  float a = 2.0 * x - 1.0;
  float b = 2.0 * y - 1.0;

  if(a > -b) {
    if(a > b) {
      r = a;
      phi = M_PI_4 *(b/a);
    }
    else {
      r = b;
      phi = M_PI_4 *(2.0 - a/b);
    }
  }
  else {
    if(a < b) {
      r = -a;
      phi = M_PI_4 *(4.0 + b/a);
    }
    else {
      r = -b;
      if(b != 0.0) phi = M_PI_4 *(6.0 - a/b);
      else phi = 0.0;
    }
  }
  x_out = r * cos(phi);
  y_out = r * sin(phi);
}

void make_orthonormals(vector N, output vector a, output vector b)
{
  if(N[0] != N[1] || N[0] != N[2]) a = cross(vector(1, 1, 1), N);
  else a = cross(vector(-1, 1, 1), N);

  a = normalize(a);
  b = cross(N, a);
}

vector sample_cos_hemisphere(vector N, float randu, float randv)
{
  vector T, B;

  make_orthonormals(N, T, B);
  to_unit_disk(randu, randv, randu, randv);
  float costheta = sqrt(max(1.0 - randu * randu - randv * randv, 0.0));

  return randu * T + randv * B + costheta * N;
}

shader BaAmbientOcclusion(
  color Effect = color(0) [[ string label = \"Effect\" ]],
  color No_Effect = color(1) [[ string label = \"No Effect\" ]],
  int Mode = 0 [[ string label = \"Mode (AO-Wear-Both)\" ]], /* 0: Concave (AO) 1:Convex (Wear) 2:Both */
  int InvertEffect = 0 [[ string widget=\"checkBox\", string label = \"Invert Effect\" ]],
  float Distance = 0.2 [[ string label = \"Distance\" ]],
  int Samples = 1 [[ string label = \"Samples\" ]],
  output color Color = 0 [[ string label = \"Color\" ]],
  output float Fac = 0 [[ string label = \"Factor\" ]],)
{
  int i, rng;
  float f, randu, randv, ray_t, hits = 0;
  vector ray_P, ray_R;

  f = fmod(cellnoise(P*123456.0), 1.0);
  rng_seed(rng, int(f * 2137483647));

  for(i = 0; i < Samples; i++) {
    randu = rng_uniform(rng);
    randv = rng_uniform(rng);

    ray_P = P;
    ray_R = sample_cos_hemisphere(-N, randu, randv);
    ray_t = Distance;

    if (!Mode) {
      if(trace(ray_P, -ray_R, \"maxdist\", ray_t)) hits += 1.0;
    }
    else if (Mode == 1) {
      if(trace(ray_P, ray_R, \"maxdist\", ray_t)) hits += 1.0;
    }
    else {
      if(trace(ray_P, -ray_R, \"maxdist\", ray_t)) hits += 1.0;
      if(trace(ray_P, ray_R, \"maxdist\", ray_t)) hits += 1.0;
    }
  }
  Fac = 1.0 - (hits/Samples);
  if(InvertEffect) Color = mix(No_Effect, Effect, Fac);
  else Color = mix(Effect, No_Effect, Fac);
}
"
		matNode.Distance = 0.05
		matNode.Samples = 150
		matNode
	),
	fn matGradientNode axis:#Z gradMin:0.0 gradMax:1.0 =
	(
		local matNode = OSLMap()
		matNode.OSLCode = "float saturate(float value)
{
	return clamp(value, 0.0, 1.0);	
}

float frac(float value)
{
	return value - floor(value);
}

shader AxisLinearGradient
(
	point  Input = P,
	string Axis = \"X\" 
		[[ string widget=\"popup\",
		   string help = \"axis\",
		   string options=\"X|Y|Z\",
		   int editable=1 ]],
	float Min = 0.0,
	float Max = 1.0,
	int   Saturate    = 1
		[[ string widget=\"checkBox\", string label = \"Saturate\" ]],
	int   Repeat    = 0
		[[ string widget=\"checkBox\", string label = \"Repeat (if not Saturate)\" ]],
	output float grad = 0.0
)
{
	float a = 0.0;
	if (Axis == \"X\") {a = Input.x;}
	if (Axis == \"Y\") {a = Input.y;}
	if (Axis == \"Z\") {a = Input.z;}
	a = (a - Min) / (Max - Min);
	if (Saturate) {
		grad = saturate(a);
	}
	else if (Repeat) {
		grad = frac(a);
	}
	else {
		grad = a;
	}
}
"
		matNode.Axis = toUpper (axis as string)
		matNode.Min = gradMin
		matNode.Max = gradMax
		matNode
	),
	fn updateMatGradientNode matNode axis: gradMin: gradMax: =
	(
		if axis != unsupplied then matNode.Axis = toUpper (axis as string)
		if gradMin != unsupplied then matNode.Min = gradMin
		if gradMax != unsupplied then matNode.Max = gradMax
	),
	fn createDebugRenderMaterial name: map:#albedoMap rendererType:#scanline albedoColor: heightMapAxis: heightMapRange:[0.0,1.0] invertNormal:false =
	(
		local newMaterial
		case rendererType of
		(
			#scanline:
			(
				newMaterial = Standardmaterial name:name
				newMaterial.selfIllumAmount = 100.0
			)
			#arnold:
			(
				newMaterial = ArnoldMapToMtl name:name
			)
		)
		local renderNode = case map of
		(
			#albedoMap:(
				if albedoColor != unsupplied then
				(
					local colorNode = asobo_planeSeatProjStruct.matColorNode()
					colorNode.In = albedoColor
					colorNode
				)
				else asobo_planeSeatProjStruct.createDebugMap()
			)
			#roughnessMap:(
				local colorNode = asobo_planeSeatProjStruct.matColorNode()
				colorNode.In = black
				colorNode
			)
			#metallicMap:(
				local colorNode = asobo_planeSeatProjStruct.matColorNode()
				colorNode.In = black
				colorNode
			)
			#emissiveMap:(
				local colorNode = asobo_planeSeatProjStruct.matColorNode()
				colorNode.In = black
				colorNode
			)
			#aoMap:(
				case rendererType of
				(
					#scanline:
					(
						-- OSL AO node keeps crashing 3dsmax randomly, replaced by white output...
-- 						local aoNode = asobo_planeSeatProjStruct.matAONode()
-- 						local aoNodeLinker = MultiOutputChannelTexmapToTexmap sourceMap:aoNode
-- 						aoNodeLinker
						local colorNode = asobo_planeSeatProjStruct.matColorNode()
						colorNode.In = white
						colorNode
					)
					#arnold:
					(
						local aoNode = ai_ambient_occlusion samples:4 black:(color 127 127 127) falloff:10.0
						aoNode
					)
				)
			)
			#normalMap:(
				local normalNode = asobo_planeSeatProjStruct.matNormalNode()
				local addNode = asobo_planeSeatProjStruct.matAddNode()
				--following get world normal between [0~1]
				addNode.A_map = normalNode
				addNode.A_Amount = 0.5
				local normalTweakNode = asobo_planeSeatProjStruct.matNormalFinalTweak invertNormal:invertNormal
				normalTweakNode.NormalMap_map = addNode
				normalTweakNode
			)
			#heightMap:(
				local coordNode = asobo_planeSeatProjStruct.matCoordNode() --didnt use coordSpace:#camera for projection
				local heightNode = asobo_planeSeatProjStruct.matGradientNode axis:heightMapAxis gradMin:heightMapRange.x gradMax:heightMapRange.y
				heightNode.Input_map = coordNode
				heightNode
			)
		)
		case rendererType of
		(
			#scanline:
			(
				newMaterial.diffuseMap = renderNode
			)
			#arnold:
			(
				newMaterial.SurfaceShader = renderNode
			)
		)
		newMaterial
	),
	fn convertSingleMaterialMapToRenderMaterial fsMaterial map:#albedoMap rendererType:#scanline heightMapAxis: heightMapRange:[0.0,1.0] = 
	(
		local newMatName = fsMaterial.name + "_Render"
		if classOf fsMaterial != MSFS2024_Material then
		(
			asobo_planeSeatProjStruct.createDebugRenderMaterial name:newMatName rendererType:rendererType heightMapAxis:heightMapAxis heightMapRange:heightMapRange
		)
		else
		(
			local newMaterial
			case rendererType of
			(
				#scanline:
				(
					newMaterial = Standardmaterial name:newMatName
					newMaterial.selfIllumAmount = 100.0
				)
				#arnold:
				(
					newMaterial = ArnoldMapToMtl name:newMatName
				)
			)
			local renderNode = case map of
			(
				#albedoMap:(
					local multiplyNode = asobo_planeSeatProjStruct.matMultiplyNode()
					local colorNode = asobo_planeSeatProjStruct.matColorNode()
					colorNode.In = fsMaterial.basecolor
					multiplyNode.A_map = colorNode
					
					if fsMaterial.BaseColorTex != undefined and fsMaterial.BaseColorTex != "" then
					(
						multiplyNode.B_map = Bitmaptexture filename:fsMaterial.BaseColorTex
					)
					multiplyNode
				)
				#roughnessMap:(
					local floatNode = asobo_planeSeatProjStruct.matFloatNode()
					local multiplyNode = asobo_planeSeatProjStruct.matMultiplyNode()
					floatNode.In = fsMaterial.roughness
					multiplyNode.A_map = floatNode
					
					if fsMaterial.OcclusionRoughnessMetallicTex != undefined and fsMaterial.OcclusionRoughnessMetallicTex != "" then
					(
						local bm = Bitmaptexture filename:fsMaterial.OcclusionRoughnessMetallicTex
						local roughnessTint = RGB_Tint map1:bm map1Enabled:true
						roughnessTint.red = (color 0 0 0)
						roughnessTint.green = (color 255 255 255)
						roughnessTint.blue = (color 0 0 0)
						multiplyNode.B_map = roughnessTint
					)
					multiplyNode
				)
				#metallicMap:(
					local floatNode = asobo_planeSeatProjStruct.matFloatNode()
					local multiplyNode = asobo_planeSeatProjStruct.matMultiplyNode()
					floatNode.In = fsMaterial.metallic
					multiplyNode.A_map = floatNode
					
					if fsMaterial.OcclusionRoughnessMetallicTex != undefined and fsMaterial.OcclusionRoughnessMetallicTex != "" then
					(
						local bm = Bitmaptexture filename:fsMaterial.OcclusionRoughnessMetallicTex
						local metallicTint = RGB_Tint map1:bm map1Enabled:true
						metallicTint.red = (color 0 0 0)
						metallicTint.green = (color 0 0 0)
						metallicTint.blue = (color 255 255 255)
						multiplyNode.B_map = metallicTint
					)
					multiplyNode
				)
				#emissiveMap:(
					local multiplyNode = asobo_planeSeatProjStruct.matMultiplyNode()
					local colorNode = asobo_planeSeatProjStruct.matColorNode()
					colorNode.In = fsMaterial.emissive
					multiplyNode.A_map = colorNode
					
					if fsMaterial.EmissiveTex != undefined and fsMaterial.EmissiveTex != "" then
					(
						multiplyNode.B_map = Bitmaptexture filename:fsMaterial.EmissiveTex
					)
					
					local multiplyNode2 = asobo_planeSeatProjStruct.matMultiplyNode()
					local floatClampNode = asobo_planeSeatProjStruct.matFloatClampNode()
					floatClampNode.Input = fsMaterial.emissiveMul --need to transfer this param manually to new material ! Only used [0-1] range to be foolproof in case == 0
					multiplyNode2.A_map = floatClampNode
					multiplyNode2.B_map = multiplyNode
					multiplyNode2
				)
				#aoMap:(
					local floatNode = asobo_planeSeatProjStruct.matFloatNode()
					local multiplyNode = asobo_planeSeatProjStruct.matMultiplyNode()
					floatNode.In = fsMaterial.occlusionStrength
					multiplyNode.A_map = floatNode
				
					local multiplyNode2 = asobo_planeSeatProjStruct.matMultiplyNode()
					local aoNode = case rendererType of
					(
						#scanline:
						(
							-- OSL AO node keeps crashing 3dsmax randomly, replaced by white output...
-- 							local aoNodeR = asobo_planeSeatProjStruct.matAONode()
-- 							local aoNodeLinker = MultiOutputChannelTexmapToTexmap sourceMap:aoNodeR
-- 							aoNodeLinker
							local colorNode = asobo_planeSeatProjStruct.matColorNode()
							colorNode.In = white
							colorNode
						)
						#arnold:
						(
							local aoNodeR = ai_ambient_occlusion samples:4 black:(color 127 127 127) falloff:10.0
							aoNodeR
						)
					)
					multiplyNode2.A_map = aoNode
					if fsMaterial.OcclusionRoughnessMetallicTex != undefined and fsMaterial.OcclusionRoughnessMetallicTex != "" then
					(
						local bm = Bitmaptexture filename:fsMaterial.OcclusionRoughnessMetallicTex
						local occlusionTint = RGB_Tint map1:bm map1Enabled:true
						occlusionTint.red = (color 255 255 255)
						occlusionTint.green = (color 0 0 0)
						occlusionTint.blue = (color 0 0 0)
						multiplyNode2.B_map = occlusionTint
-- 						multiplyNode.B_map = occlusionTint
					)
					multiplyNode.B_map = multiplyNode2
					multiplyNode
				)
				#normalMap:(
					local normalNode = asobo_planeSeatProjStruct.matNormalNode()
					local addNode = asobo_planeSeatProjStruct.matAddNode()
					--following get world normal between [0~1]
					addNode.A_map = normalNode
					addNode.A_Amount = 0.5
					local normalTweakNode = asobo_planeSeatProjStruct.matNormalFinalTweak()
					normalTweakNode.NormalMap_map =
					if fsMaterial.NormalTex != undefined and fsMaterial.NormalTex != "" then
					(
						local bm = Bitmaptexture filename:fsMaterial.NormalTex
						--following get texture normal
						local normalFixNode = asobo_planeSeatProjStruct.matNormalTangentToWorldNode()
						normalFixNode.NormalMap_map = bm
						--lerp between texture normal and world normal
						local floatNode = asobo_planeSeatProjStruct.matFloatNode()
						local lerpNode = asobo_planeSeatProjStruct.matLerpNode()
						floatNode.In = fsMaterial.normalScale
						lerpNode.Input_map = floatNode
						lerpNode.Min_map = addNode
						lerpNode.Max_map = normalFixNode
						lerpNode
					)
					else
					(
						addNode
					)
					normalTweakNode
				)
				#heightMap:(
					local coordNode = asobo_planeSeatProjStruct.matCoordNode() --didnt use coordSpace:#camera for projection
					local heightNode = asobo_planeSeatProjStruct.matGradientNode axis:heightMapAxis gradMin:heightMapRange.x gradMax:heightMapRange.y
					heightNode.Input_map = coordNode
					heightNode
				)
			)
			case rendererType of
			(
				#scanline:
				(
					newMaterial.diffuseMap = renderNode
				)
				#arnold:
				(
					newMaterial.SurfaceShader = renderNode
				)
			)
			newMaterial
		)
	),
	fn convertMaterialToRenderMaterial mat map:#albedoMap rendererType:#scanline heightMapAxis: heightMapRange: =
	(
		if classOf mat == Multimaterial then
		(
			local subMatNb = mat.numsubs
			local newMultiMat = Multimaterial numsubs:subMatNb
			local matSubMats = mat.materialList
			for i = 1 to subMatNb do newMultiMat.material[i] = asobo_planeSeatProjStruct.convertSingleMaterialMapToRenderMaterial matSubMats[i] map:map rendererType:rendererType heightMapAxis:heightMapAxis heightMapRange:heightMapRange
			newMultiMat
		)
		else
		(
			asobo_planeSeatProjStruct.convertSingleMaterialMapToRenderMaterial mat map:map heightMapAxis:heightMapAxis heightMapRange:heightMapRange
		)
	),
	fn convertNodeMaterialToRenderMaterial n &existingMat map:#albedoMap rendererType:#scanline heightMapAxis: heightMapRange: debugNoMaterial:true =
	(
		local mat = n.material
		if mat != undefined then
		(
			if existingMat == undefined then existingMat = asobo_planeSeatProjStruct.convertMaterialToRenderMaterial mat map:map rendererType:rendererType heightMapAxis:heightMapAxis heightMapRange:heightMapRange
			n.material = existingMat
		)
		else if debugNoMaterial then
		(
			n.material = asobo_planeSeatProjStruct.createDebugRenderMaterial name:"Debug material" map:map rendererType:rendererType heightMapAxis:heightMapAxis heightMapRange:heightMapRange
		)
	),
	
	/* BITMAP MANIPULATION */
	fn rgbFrom1AFrom2Premult color1 pos1 color2 pos2 =
	(
		(color color2.r color2.g color2.b color1.v)
	),
	fn rgbFrom1AFrom2 color1 pos1 color2 pos2 =
	(
		local newAlpha = color1.v
		local alphaMult = newAlpha / 255.0
		(color (color2.r * alphaMult) (color2.g * alphaMult) (color2.b * alphaMult) newAlpha)
	),
	--compose bitmaps using pasteBitmap
	-- about as fast as getPixels/setPixelsis if premultiplied
	-- *a little bit* faster with non-premultiplied alpha, but it fails miserably to be 100% accurate when compositing
	fn bmToRGBBm2ToA_alternative bm bm2 premultiplied:true =
	(
		if premultiplied then
			pasteBitmap bm2 bm [0,0] [0,0] type:#function function:asobo_planeSeatProjStruct.rgbFrom1AFrom2Premult
		else
			pasteBitmap bm2 bm [0,0] [0,0] type:#function function:asobo_planeSeatProjStruct.rgbFrom1AFrom2
		bm
	),
	--100% accurate when compositing with premultiplied AND non-premultiplied alpha
	fn bmToRGBBm2ToA bm bm2 premultiplied:true =
	(
		local nBm = bitmap (bm.width) (bm.height) color:(color 255 255 255 0) gamma:bm.gamma
		local w = bm.width
		local h = bm.height
		if premultiplied then
		(
			for y = 0 to h - 1 do
			(
				local row = getPixels bm [0,y] w linear:(bm.gamma == 1.0)
				local row2 = getPixels bm2 [0,y] w linear:(bm2.gamma == 1.0)
				for x = 1 to w do
				(
					row[x].a = row2[x].v
				)
				setPixels nBm [0,y] row
			)
		)
		else
		(
			for y = 0 to h - 1 do
			(
				local row = getPixels bm [0,y] w linear:(bm.gamma == 1.0)
				local row2 = getPixels bm2 [0,y] w linear:(bm2.gamma == 1.0)
				for x = 1 to w do
				(
-- 					local multAlpha = row[x].a / 255.0 --original alpha -> dont premultiply, we want to keep it untouched !!
					row[x].a = row2[x].v
					local multAlpha = row[x].a / 255.0 --new alpha -> premultiply, we want to composite so we need to remove its influence here
					row[x].r *= multAlpha
					row[x].g *= multAlpha
					row[x].b *= multAlpha
				)
				setPixels nBm [0,y] row
			)
		)
		close bm
		close bm2
		nBm
	),
	fn combineBitmapFiles colorBmPath alphaBmPath bmGamma: bm2Gamma: =
	(
		local isAlphaPremultiplied = case (asobo_planeSeatProjStruct.getAfterDotFilenameTypeName colorBmPath) of
		(
			#tiff:	true
			#tga:	Targa.getPreMultAlpha()
			#png:	true
		)
		local savedBm = openBitMap colorBmPath gamma:(if bmGamma != unsupplied then bmGamma else #auto)
		local bm = copy savedBm
		close savedBm
		savedBm = openBitMap alphaBmPath gamma:(if bm2Gamma != unsupplied then bm2Gamma else #auto)
		local bm2 = copy savedBm
		close savedBm
		asobo_planeSeatProjStruct.bmToRGBBm2ToA bm bm2 premultiplied:isAlphaPremultiplied
	),
	fn createCombinedMaps texFilenames combinedTexFilenames activeMergeTextures =
	(
		/*-- combine height with ao
		if texFilenames.heightMap != undefined	and texFilenames.aoMap != undefined then
		(
			if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.heightMap	and asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.aoMap then
			(
				local heightAo = asobo_planeSeatProjStruct.combineBitmapFiles texFilenames.heightMap texFilenames.aoMap bmGamma:1.0 bm2Gamma:1.0
				heightAo.filename = combinedTexFilenames.heightAoMap
				save heightAo gamma:heightAo.gamma
				close heightAo
			)
		)*/
		/*
		-- combine normal with height
		if texFilenames.normalMap != undefined	and texFilenames.heightMap != undefined then
		(
			if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.normalMap	and asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.heightMap then
			(
				local normalHeight = asobo_planeSeatProjStruct.combineBitmapFiles texFilenames.normalMap texFilenames.heightMap bmGamma:1.0 bm2Gamma:1.0
				normalHeight.filename = combinedTexFilenames.normalHeightMap
				save normalHeight gamma:normalHeight.gamma
				close normalHeight
			)
		)*/
		-- combine normal with ao
		if texFilenames.normalMap != undefined	and texFilenames.aoMap != undefined and activeMergeTextures.normalAoMap then
		(
			if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.normalMap	and asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.aoMap then
			(
				local normalAo = asobo_planeSeatProjStruct.combineBitmapFiles texFilenames.normalMap texFilenames.aoMap bmGamma:1.0 bm2Gamma:1.0
				normalAo.filename = combinedTexFilenames.normalAoMap
				save normalAo gamma:normalAo.gamma
				close normalAo
			)
		)
		/*-- combine albedo with ao
		if texFilenames.albedoMap != undefined	and texFilenames.aoMap != undefined then
		(
			if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.albedoMap	and asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.aoMap then
			(
				local albedoAo = asobo_planeSeatProjStruct.combineBitmapFiles texFilenames.albedoMap texFilenames.aoMap bmGamma:1.0 bm2Gamma:1.0
				albedoAo.filename = combinedTexFilenames.albedoAoMap
				save albedoAo gamma:albedoAo.gamma
				close albedoAo
			)
		)*/
		-- combine albedo with height
		if texFilenames.albedoMap != undefined	and texFilenames.heightMap != undefined and activeMergeTextures.albedoHeightMap then
		(
			if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.albedoMap	and asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.heightMap then
			(
				local albedoHeight = asobo_planeSeatProjStruct.combineBitmapFiles texFilenames.albedoMap texFilenames.heightMap bmGamma:1.0 bm2Gamma:1.0
				albedoHeight.filename = combinedTexFilenames.albedoHeightMap
				save albedoHeight gamma:albedoHeight.gamma
				close albedoHeight
			)
		)
		-- if texFilenames.emissiveMap != undefined	then if asobo_planeSeatProjStruct.doesFileExistSafe texFilenames.emissiveMap	then ()
	),
	
	/* MAP RENDER */
	fn getBleedValue texSize =
	(
		(asobo_planeSeatProjStruct.roundNb (((amax texSize.x texSize.y) as float) / 64.0)) as integer
	),
	fn getSafeTextureSize texSizeVector dxtSafe:false =
	(
		
		local safeMinSize = if dxtSafe then 4 else 1 -- need minimum 1px size for bitmap render or 4 for DXT compression
		local safeTexVector = asobo_planeSeatProjStruct.maxVector texSizeVector safeMinSize
		if dxtSafe then safeTexVector = asobo_planeSeatProjStruct.upMultipleVector safeTexVector multiple:4
		safeTexVector = asobo_planeSeatProjStruct.intVector safeTexVector -- just to be safe
		safeTexVector
	),
	fn setupBakeMap map size filename name =
	(
		case classOf map of
		(
			NormalsMap:
			(
				map.useNormalBump = true
				map.useHeightAsAlpha = true
				map.backgroundColor = (color 128 128 255)
			)
			Ambient_Occlusion:
			(
				map.samples = 16 --integer
				map.bright = white
				map.dark = black
				map.spread = 16.0 --float
				map.maxDistance = 16.0 --float
				map.falloff = 4.0 --float
				map.backgroundColor = white
			)
			HeightMap:
			(
				map.backgroundColor = black
			)
			DiffuseMap:
			(
				map.lightingOn = false
				map.shadowsOn = false
				map.backgroundColor = black
			)
		)
		
		-- common properties
		map.enabled = true
		map.filterOn = true
		map.outputSzX = size.x
		map.outputSzY = size.y
		map.autoSzOn = false
		map.fileType = filename
		map.fileName = filenameFromPath filename
		map.filenameUnique = false
		map.elementName = name
-- 		map.bitmap =
-- 		map.targetMapSlotName =
	),
	fn createBakeMap type size filename renderInfos =
	(
		local newBakeMap = case type of
		(
			#normalMap:		if renderInfos.normal.projectionType == #customMap then DiffuseMap() else NormalsMap()
			#heightMap:		if renderInfos.height.projectionType == #customMap then DiffuseMap() else HeightMap()
			#aoMap:			if renderInfos.ao.projectionType == #customMap then DiffuseMap() else Ambient_Occlusion()
			#emissiveMap:	DiffuseMap()
			#albedoMap:		DiffuseMap()
		)
		asobo_planeSeatProjStruct.setupBakeMap newBakeMap size filename (asobo_planeSeatProjStruct.getName type)
		newBakeMap
	),
	fn setupPlaneBakeMap projPlane renderInfos type:#albedoMap =
	(
		-- setup baking
		local bakeMap =	case type of
		(
			#normalMap:		asobo_planeSeatProjStruct.createBakeMap type projPlane.bugFixTexSize projPlane.texFilenames.normalMap	renderInfos
			#heightMap:		asobo_planeSeatProjStruct.createBakeMap type projPlane.bugFixTexSize projPlane.texFilenames.heightMap	renderInfos
			#aoMap:			asobo_planeSeatProjStruct.createBakeMap type projPlane.bugFixTexSize projPlane.texFilenames.aoMap		renderInfos
			#emissiveMap:	asobo_planeSeatProjStruct.createBakeMap type projPlane.bugFixTexSize projPlane.texFilenames.emissiveMap	renderInfos
			#albedoMap:		asobo_planeSeatProjStruct.createBakeMap type projPlane.bugFixTexSize projPlane.texFilenames.albedoMap	renderInfos
		)
		projPlane.projPlane.INodeBakeProperties.addBakeElement bakeMap
		
		projPlane.projPlane.INodeBakeProperties.bakeEnabled = true --enabling baking
		projPlane.projPlane.INodeBakeProperties.bakeChannel = 1 --channel to bake
		projPlane.projPlane.INodeBakeProperties.nDilations = asobo_planeSeatProjStruct.getBleedValue projPlane.texSize --bleed value
		projPlane.projPlane.INodeBakeProperties.activeWidth = projPlane.bugFixTexSize.x --this seems not needed but added anyway.
		projPlane.projPlane.INodeBakeProperties.activeHeight = projPlane.bugFixTexSize.y --this seems not needed but added anyway.
		
		projPlane.projPlane.INodeBakeProjProperties.enabled = true
		projPlane.projPlane.INodeBakeProjProperties.projectionMod = projPlane.projMod
-- 		projPlane.projPlane.INodeBakeProjProperties.projectionModTarget = --string
		projPlane.projPlane.INodeBakeProjProperties.cropAlpha = false
		projPlane.projPlane.INodeBakeProjProperties.projSpace = #raytrace --#raytrace|#uvw_match
		projPlane.projPlane.INodeBakeProjProperties.normalSpace = #world --#world|#screen|#local|#tangent
		projPlane.projPlane.INodeBakeProjProperties.tangentYDir = #Y_Up --#Y_Up|#Y_Down
		projPlane.projPlane.INodeBakeProjProperties.tangentXDir = #X_Right --#X_Right|#X_Left
		projPlane.projPlane.INodeBakeProjProperties.useCage = false
		projPlane.projPlane.INodeBakeProjProperties.rayOffset = 0.0
		projPlane.projPlane.INodeBakeProjProperties.hitResolveMode = #furthest --#closest|#furthest
		projPlane.projPlane.INodeBakeProjProperties.hitMatchMtlID = false
		projPlane.projPlane.INodeBakeProjProperties.hitWorkingModel = false
		projPlane.projPlane.INodeBakeProjProperties.warnRayMiss = true
		projPlane.projPlane.INodeBakeProjProperties.rayMissColor = case type of (
			#normalMap:	(color 127 127 255)
			default:	black
		)
		projPlane.projPlane.INodeBakeProjProperties.heightMapMin = -projPlane.zSize
		projPlane.projPlane.INodeBakeProjProperties.heightMapMax = 0.0
-- 		projPlane.projPlane.INodeBakeProjProperties.heightBufMin = 0.0
-- 		projPlane.projPlane.INodeBakeProjProperties.heightBufMax = 0.0
		projPlane.projPlane.INodeBakeProjProperties.BakeObjectLevel = true
		projPlane.projPlane.INodeBakeProjProperties.BakeSubObjLevels = false
-- 		projPlane.projPlane.INodeBakeProjProperties.useObjectBakeForMtl = true --or BakeSubObjLevels
-- 		projPlane.projPlane.INodeBakeProjProperties.proportionalOutput = true --for BakeSubObjLevels
-- 		projPlane.projPlane.INodeBakeProjProperties.subObjBakeChannel = 1 --for BakeSubObjLevels
	),
	fn setupPlaneBakeMaps projPlanes renderInfos =
	(
		if renderInfos.normal.active	and renderInfos.normal.renderType == #projection		then asobo_planeSeatProjStruct.setupPlaneBakeMap projPlanes.normal		renderInfos	type:#normalMap
		if renderInfos.height.active	and renderInfos.height.renderType == #projection		then asobo_planeSeatProjStruct.setupPlaneBakeMap projPlanes.height		renderInfos	type:#heightMap
		if renderInfos.ao.active		and renderInfos.ao.renderType == #projection			then asobo_planeSeatProjStruct.setupPlaneBakeMap projPlanes.ao			renderInfos	type:#aoMap
		if renderInfos.emissive.active	and renderInfos.emissive.renderType == #projection		then asobo_planeSeatProjStruct.setupPlaneBakeMap projPlanes.emissive	renderInfos	type:#emissiveMap
		if renderInfos.albedo.active	and renderInfos.albedo.renderType == #projection		then asobo_planeSeatProjStruct.setupPlaneBakeMap projPlanes.albedo		renderInfos	type:#albedoMap
	),
	fn bakeMaps projPlane &renderWasCancelled showRendering: =
	(
		if projPlane != undefined then
		(
			case projPlane.rendererType of
			(
				#scanline:
				(
					if classOf renderers.current != Default_Scanline_Renderer then renderers.current = Default_Scanline_Renderer()
				)
				#arnold:
				(
					if classOf renderers.current != Arnold then renderers.current = Arnold()
				)
			)
			
			-- Bugfix
			local needBugFix = projPlane.texSize != projPlane.bugFixTexSize
			local vfbDisplay = if showRendering != unsupplied then showRendering else false
			
			select projPlane.projPlane -- we are baking the selection, so we select the object
			
			if needBugFix then
			(
				local renderNb = projPlane.projPlane.INodeBakeProperties.numBakeElements()
				local bakeElts = for i = 1 to renderNb collect projPlane.projPlane.INodeBakeProperties.getBakeElement i
				for i = 1 to renderNb do
				(
					projPlane.projPlane.INodeBakeProperties.removeAllBakeElements()
					projPlane.projPlane.INodeBakeProperties.addBakeElement bakeElts[i]
					local renderedBitmap
					if classOf renderers.current == Default_Scanline_Renderer then
					(
						render rendertype:#bakeSelected vfb:vfbDisplay progressBar:true cancelled:&renderWasCancelled outputSize:projPlane.bugFixTexSize \
							renderhiddenobjects:true quiet:true
						if not renderWasCancelled then
						(
							local writtenRendered = openBitMap (bakeElts[i].fileType)
							renderedBitmap = copy writtenRendered
							close writtenRendered
						)
					)
					else
					(
						renderedBitmap = render rendertype:#bakeSelected vfb:vfbDisplay progressBar:true cancelled:&renderWasCancelled outputSize:projPlane.bugFixTexSize \
											renderhiddenobjects:true quiet:true
					)
					if not renderWasCancelled then
					(
						local fixedBitmap = bitmap projPlane.texSize.x projPlane.texSize.y filename:(bakeElts[i].fileType) gamma:renderedBitmap.gamma pixelAspect:renderedBitmap.aspect channels:renderedBitmap.channels --hdr:<boolean>
						local cropArea = box2 ((projPlane.bugFixTexSize.x - projPlane.texSize.x) / 2) ((projPlane.bugFixTexSize.y - projPlane.texSize.y) / 2) projPlane.texSize.x projPlane.texSize.y
						pasteBitmap renderedBitmap fixedBitmap cropArea [0,0] type:#paste
						close renderedBitmap
						save fixedBitmap
						close fixedBitmap
					)
				)
			)
			else
			(
				render rendertype:#bakeSelected vfb:vfbDisplay progressBar:true cancelled:&renderWasCancelled outputSize:projPlane.bugFixTexSize \
					renderhiddenobjects:true quiet:true
			)
		)
	),
	
	/* CAMERA RENDERING */
	projectionCameras = struct projectionCameras
	(
		normal,
		height,
		ao,
		emissive,
		albedo
	);,
	projectionCamera = struct projectionCamera
	(
		projCamera,
		projObjs,
		texSize,
		bugFixTexSize,
		texFilename,
		rendererType
	);,
	fn createFittingCamera pos axis size texSize bugFixTexSize texFilename projObjs rendererType name: layer: =
	(
		local fov = 45.0
		local fovType = 1 --horizontal|vertical|diagonal
		local cameraDistance = (size.x / 2.0) / (tan (radToDeg (PI * fov / 360.0))) --used horizontal fovType -> used width size value
		local cameraPos = case axis of
		(
			#plusX:		pos + [cameraDistance, 0, 0]
			#plusY:		pos - [0, cameraDistance, 0]
			#plusZ:		pos + [0, 0, cameraDistance]
			#minusX:	pos - [cameraDistance, 0, 0]
			#minusY:	pos + [0, cameraDistance, 0]
			#minusZ:	pos - [0, 0, cameraDistance]
		)
		local newCamera = Freecamera name:name position:cameraPos fov:fov nearClip:cameraDistance farClip:(cameraDistance + size.z) fovType:fovType orthoProjection:true
		newCamera.baseObject.targetDistance = cameraDistance --just for visual debug
		asobo_planeSeatProjStruct.objectRotationToAxis newCamera axis
		if layer != unsupplied then layer.addNode newCamera
		(asobo_planeSeatProjStruct()).projectionCamera projCamera:newCamera projObjs:projObjs texSize:texSize bugFixTexSize:bugFixTexSize texFilename:texFilename rendererType:rendererType
	),
	fn createFittingCameras pos axis size texSize bugFixTexSize texFilenames projObjs backPlanes renderInfos name: layer: =
	(
		local renderCameras = (asobo_planeSeatProjStruct()).projectionCameras()
		if renderInfos.normal.active	and renderInfos.normal.renderType == #camera		then renderCameras.normal = asobo_planeSeatProjStruct.createFittingCamera pos axis size texSize bugFixTexSize texFilenames.normalMap (projObjs.normal+#(backPlanes.normal)) renderInfos.normal.rendererType name:(name + "_normal") layer:layer
		if renderInfos.height.active	and renderInfos.height.renderType == #camera		then renderCameras.height = asobo_planeSeatProjStruct.createFittingCamera pos axis size texSize bugFixTexSize texFilenames.heightMap (projObjs.height+#(backPlanes.height)) renderInfos.height.rendererType name:(name + "_height") layer:layer
		if renderInfos.ao.active		and renderInfos.ao.renderType == #camera			then renderCameras.ao = asobo_planeSeatProjStruct.createFittingCamera pos axis size texSize bugFixTexSize texFilenames.aoMap projObjs.ao renderInfos.ao.rendererType name:(name + "_ao") layer:layer
		if renderInfos.emissive.active	and renderInfos.emissive.renderType == #camera		then renderCameras.emissive = asobo_planeSeatProjStruct.createFittingCamera pos axis size texSize bugFixTexSize texFilenames.emissiveMap projObjs.emissive renderInfos.emissive.rendererType name:(name + "_emissive") layer:layer
		if renderInfos.albedo.active	and renderInfos.albedo.renderType == #camera		then renderCameras.albedo = asobo_planeSeatProjStruct.createFittingCamera pos axis size texSize bugFixTexSize texFilenames.albedoMap projObjs.albedo renderInfos.albedo.rendererType name:(name + "_albedo") layer:layer
		renderCameras
	),
	fn cameraRenderMaps projCamera &renderWasCancelled showRendering: =
	(
		if projCamera != undefined then
		(
			case projCamera.rendererType of
			(
				#scanline:
				(
					if classOf renderers.current != Default_Scanline_Renderer then renderers.current = Default_Scanline_Renderer()
				)
				#arnold:
				(
					if classOf renderers.current != Arnold then renderers.current = Arnold()
				)
			)
			
			-- Bugfix
			local needBugFix = projCamera.texSize != projCamera.bugFixTexSize
			local vfbDisplay = if showRendering != unsupplied then showRendering else false
			
			select projCamera.projObjs -- we are baking the selection, so we select the objects
			
			if needBugFix then
			(
				local renderedBitmap = render rendertype:#selected camera:projCamera.projCamera vfb:vfbDisplay progressBar:true cancelled:&renderWasCancelled outputSize:projCamera.bugFixTexSize \
										renderhiddenobjects:true quiet:true
				if not renderWasCancelled then
				(
					local fixedBitmap = bitmap projCamera.texSize.x projCamera.texSize.y filename:projCamera.texFilename gamma:renderedBitmap.gamma pixelAspect:renderedBitmap.aspect channels:renderedBitmap.channels --hdr:<boolean>
					local cropArea = box2 ((projCamera.bugFixTexSize.x - projCamera.texSize.x) / 2) ((projCamera.bugFixTexSize.y - projCamera.texSize.y) / 2) projCamera.texSize.x projCamera.texSize.y
					pasteBitmap renderedBitmap fixedBitmap cropArea [0,0] type:#paste
					close renderedBitmap
					save fixedBitmap
					close fixedBitmap
				)
			)
			else
			(
				render rendertype:#selected camera:projCamera.projCamera vfb:vfbDisplay progressBar:true cancelled:&renderWasCancelled outputfile:projCamera.texFilename outputSize:projCamera.bugFixTexSize \
					renderhiddenobjects:true quiet:true
			)
		)
	),
	
	/* RENDER */
	fn renderMaps projPlanes projCameras gammaIn gammaOut &renderWasCancelled showRendering: =
	(
		if not renderWasCancelled then
		(
			fileInGamma = 1.0
			fileOutGamma = 1.0
			asobo_planeSeatProjStruct.bakeMaps 			projPlanes.normal		&renderWasCancelled showRendering:showRendering
			asobo_planeSeatProjStruct.cameraRenderMaps	projCameras.normal		&renderWasCancelled showRendering:showRendering
		)
		if not renderWasCancelled then
		(
			fileInGamma = 1.0
			fileOutGamma = 1.0
			asobo_planeSeatProjStruct.bakeMaps 			projPlanes.height		&renderWasCancelled showRendering:showRendering
			asobo_planeSeatProjStruct.cameraRenderMaps	projCameras.height		&renderWasCancelled showRendering:showRendering
		)
		if not renderWasCancelled then
		(
			fileInGamma = 1.0
			fileOutGamma = 1.0
			asobo_planeSeatProjStruct.bakeMaps 			projPlanes.ao			&renderWasCancelled showRendering:showRendering
			asobo_planeSeatProjStruct.cameraRenderMaps	projCameras.ao			&renderWasCancelled showRendering:showRendering
		)
		if not renderWasCancelled then
		(
			fileInGamma = gammaIn
			fileOutGamma = gammaOut
			asobo_planeSeatProjStruct.bakeMaps 			projPlanes.emissive		&renderWasCancelled showRendering:showRendering
			asobo_planeSeatProjStruct.cameraRenderMaps	projCameras.emissive	&renderWasCancelled showRendering:showRendering
		)
		if not renderWasCancelled then
		(
			fileInGamma = gammaIn
			fileOutGamma = gammaOut
			asobo_planeSeatProjStruct.bakeMaps 			projPlanes.albedo		&renderWasCancelled showRendering:showRendering
			asobo_planeSeatProjStruct.cameraRenderMaps	projCameras.albedo		&renderWasCancelled showRendering:showRendering
		)
	),
	
	/* FILTER FOR RENDER */
	fn filterPlanesByRendererType projPlanes renderInfos rendererType =
	(
		filteredPlanes = (asobo_planeSeatProjStruct()).projectionPlanes()
		if renderInfos.normal.renderType == #projection and renderInfos.normal.rendererType == rendererType then
			filteredPlanes.normal = (asobo_planeSeatProjStruct()).projectionPlane projPlane:projPlanes.normal.projPlane \
				texSize:projPlanes.normal.texSize \
				bugFixTexSize:projPlanes.normal.bugFixTexSize \
				zSize:projPlanes.normal.zSize \
				texFilenames:projPlanes.normal.texFilenames \
				projMod:projPlanes.normal.projMod \
				rendererType:projPlanes.normal.rendererType
		if renderInfos.height.renderType == #projection and renderInfos.height.rendererType == rendererType then
			filteredPlanes.height = (asobo_planeSeatProjStruct()).projectionPlane projPlane:projPlanes.height.projPlane \
				texSize:projPlanes.height.texSize \
				bugFixTexSize:projPlanes.height.bugFixTexSize \
				zSize:projPlanes.height.zSize \
				texFilenames:projPlanes.height.texFilenames \
				projMod:projPlanes.height.projMod \
				rendererType:projPlanes.height.rendererType
		if renderInfos.ao.renderType == #projection and renderInfos.ao.rendererType == rendererType then
			filteredPlanes.ao = (asobo_planeSeatProjStruct()).projectionPlane projPlane:projPlanes.ao.projPlane \
				texSize:projPlanes.ao.texSize \
				bugFixTexSize:projPlanes.ao.bugFixTexSize \
				zSize:projPlanes.ao.zSize \
				texFilenames:projPlanes.ao.texFilenames \
				projMod:projPlanes.ao.projMod \
				rendererType:projPlanes.ao.rendererType
		if renderInfos.emissive.renderType == #projection and renderInfos.emissive.rendererType == rendererType then
			filteredPlanes.emissive = (asobo_planeSeatProjStruct()).projectionPlane projPlane:projPlanes.emissive.projPlane \
				texSize:projPlanes.emissive.texSize \
				bugFixTexSize:projPlanes.emissive.bugFixTexSize \
				zSize:projPlanes.emissive.zSize \
				texFilenames:projPlanes.emissive.texFilenames \
				projMod:projPlanes.emissive.projMod \
				rendererType:projPlanes.emissive.rendererType
		if renderInfos.albedo.renderType == #projection and renderInfos.albedo.rendererType == rendererType then
			filteredPlanes.albedo = (asobo_planeSeatProjStruct()).projectionPlane projPlane:projPlanes.albedo.projPlane \
				texSize:projPlanes.albedo.texSize \
				bugFixTexSize:projPlanes.albedo.bugFixTexSize \
				zSize:projPlanes.albedo.zSize \
				texFilenames:projPlanes.albedo.texFilenames \
				projMod:projPlanes.albedo.projMod \
				rendererType:projPlanes.albedo.rendererType
		filteredPlanes
	),
	fn filterCamerasByRendererType projCameras renderInfos rendererType =
	(
		filteredCameras = (asobo_planeSeatProjStruct()).projectionCameras()
		if renderInfos.normal.active and renderInfos.normal.renderType == #camera and renderInfos.normal.rendererType == rendererType then
			filteredCameras.normal = (asobo_planeSeatProjStruct()).projectionCamera projCamera:projCameras.normal.projCamera \
				projObjs:projCameras.normal.projObjs \
				texSize:projCameras.normal.texSize \
				bugFixTexSize:projCameras.normal.bugFixTexSize \
				texFilename:projCameras.normal.texFilename \
				rendererType:projCameras.normal.rendererType
		if renderInfos.height.active and renderInfos.height.renderType == #camera and renderInfos.height.rendererType == rendererType then
			filteredCameras.height = (asobo_planeSeatProjStruct()).projectionCamera projCamera:projCameras.height.projCamera \
				projObjs:projCameras.height.projObjs \
				texSize:projCameras.height.texSize \
				bugFixTexSize:projCameras.height.bugFixTexSize \
				texFilename:projCameras.height.texFilename \
				rendererType:projCameras.height.rendererType
		if renderInfos.ao.active and renderInfos.ao.renderType == #camera and renderInfos.ao.rendererType == rendererType then
			filteredCameras.ao = (asobo_planeSeatProjStruct()).projectionCamera projCamera:projCameras.ao.projCamera \
				projObjs:projCameras.ao.projObjs \
				texSize:projCameras.ao.texSize \
				bugFixTexSize:projCameras.ao.bugFixTexSize \
				texFilename:projCameras.ao.texFilename \
				rendererType:projCameras.ao.rendererType
		if renderInfos.emissive.active and renderInfos.emissive.renderType == #camera and renderInfos.emissive.rendererType == rendererType then
			filteredCameras.emissive = (asobo_planeSeatProjStruct()).projectionCamera projCamera:projCameras.emissive.projCamera \
				projObjs:projCameras.emissive.projObjs \
				texSize:projCameras.emissive.texSize \
				bugFixTexSize:projCameras.emissive.bugFixTexSize \
				texFilename:projCameras.emissive.texFilename \
				rendererType:projCameras.emissive.rendererType
		if renderInfos.albedo.active and renderInfos.albedo.renderType == #camera and renderInfos.albedo.rendererType == rendererType then
			filteredCameras.albedo = (asobo_planeSeatProjStruct()).projectionCamera projCamera:projCameras.albedo.projCamera \
				projObjs:projCameras.albedo.projObjs \
				texSize:projCameras.albedo.texSize \
				bugFixTexSize:projCameras.albedo.bugFixTexSize \
				texFilename:projCameras.albedo.texFilename \
				rendererType:projCameras.albedo.rendererType
		filteredCameras
	),
	
	/* MAIN */
	fn fixSceneState =
	(
		if getCommandPanelTaskMode() == #modify and subObjectLevel != 0 then subObjectLevel = 0
	),
	renderInfos = struct renderInfos
	(
		renderAxis,
		normal,
		height,
		ao,
		emissive,
		albedo
	);,
	renderInfo = struct renderInfo
	(
		active,
		temp,
		renderType,
		projectionType,
		rendererType
	);,
	-- NOTE: If output texture size axis (x or y) < 2 * pxMargin, margin will be wrong on that axis (ex: can't add 1px margin on 2px !)
	fn getModelProjTextures
	renderAxis:(#(#top, #back, #front, #side))
	renderTextures:(#(#normalMap, #heightMap, #aoMap, #emissiveMap, #albedoMap))
	mergeTextures:(#(#albedoHeightMap, #normalAoMap))
	filename:
	useTextureArrayFolder:false
	forceBitmapSaveOptions:true --let user choose some of the file format save options (metadata, premultiplied alpha...) or force these too
	keepTempMergeTextures:false --keep textures used to create merged textures
	objs:(getCurrentSelection())
	maxTextureSize:1024
	pxMargin:4
	dxtSafe:true
	showRendering: =
	(
		local validObjs = asobo_planeSeatProjStruct.filterObjects objs
		if validObjs.count == 0 then asobo_planeSeatProjStruct.mBox #noValidObjectSelected
		else
		(
			local defaultFileExt = "tif"
			local activeTextures = (asobo_planeSeatProjStruct()).textureFilenames normalMap:false heightMap:false aoMap:false emissiveMap:false albedoMap:false
			for tex in renderTextures do
			(
				case tex of
				(
					#normalMap:		activeTextures.normalMap =		true
					#heightMap:		activeTextures.heightMap =		true
					#aoMap:			activeTextures.aoMap =			true
					#emissiveMap:	activeTextures.emissiveMap =	true
					#albedoMap:		activeTextures.albedoMap =		true
				)
			)
			local tempTextures = (asobo_planeSeatProjStruct()).textureFilenames normalMap:false heightMap:false aoMap:false emissiveMap:false albedoMap:false
			local activeMergeTextures = (asobo_planeSeatProjStruct()).combinedTextureFilenames normalAoMap:false albedoHeightMap:false
			local mergeTexturesPhaseActive = false
			for tex in mergeTextures do
			(
				case tex of
				(
					#albedoHeightMap:
					(
						if activeTextures.albedoMap and activeTextures.heightMap then
						(
							mergeTexturesPhaseActive = true
							activeMergeTextures.albedoHeightMap =	true
							tempTextures.albedoMap =	true
							tempTextures.heightMap =	true
						)
					)
					#normalAoMap:
					(
						if activeTextures.normalMap and activeTextures.aoMap then
						(
							mergeTexturesPhaseActive = true
							activeMergeTextures.normalAoMap =		true
							tempTextures.normalMap =	true
							tempTextures.aoMap =		true
						)
					)
				)
			)
			-- render setup
			-- renderType:		#camera|#projection --using projection here may be VERY SLOW for some reason, prefer camera
			-- projectionType:	#default|#customMap --used in conjonction with #projection - whether to use the default projection map type or replace by custom shader applied on diffuse
			-- rendererType:	#scanline|#arnold --scanline tends to execute faster than arnold
			-- note: using scanline for AO will only output texture baked AO, arnold will mix baked and real AO
			local renderInfos = (asobo_planeSeatProjStruct()).renderInfos \
				renderAxis:	(makeUniqueArray renderAxis) \
				normal:		((asobo_planeSeatProjStruct()).renderInfo active:activeTextures.normalMap	temp:tempTextures.normalMap		renderType:#camera 		projectionType:#customMap	rendererType:#scanline) \
				height:		((asobo_planeSeatProjStruct()).renderInfo active:activeTextures.heightMap	temp:tempTextures.heightMap		renderType:#camera		projectionType:#customMap	rendererType:#scanline) \
				ao:			((asobo_planeSeatProjStruct()).renderInfo active:activeTextures.aoMap		temp:tempTextures.aoMap			renderType:#camera		projectionType:#customMap	rendererType:#arnold) \
				emissive:	((asobo_planeSeatProjStruct()).renderInfo active:activeTextures.emissiveMap	temp:tempTextures.emissiveMap	renderType:#camera 		projectionType:#customMap	rendererType:#scanline) \
				albedo:		((asobo_planeSeatProjStruct()).renderInfo active:activeTextures.albedoMap	temp:tempTextures.albedoMap		renderType:#camera 		projectionType:#customMap	rendererType:#scanline)
			
			-- setup fileNames
			if filename == unsupplied then filename = "projectionTexture."+defaultFileExt
			local texFilePath = asobo_planeSeatProjStruct.addFilePathEndSlash (asobo_planeSeatProjStruct.fixFilePath (getFilenamePath filename))
			local texFileName = getFilenameFile filename
			local texFileExtension = getFilenameType filename
			
			local topAxisTexFilenames, backAxisTexFilenames, frontAxisTexFilenames, sideAxisTexFilenames
			for renderAxis in renderInfos.renderAxis do
			(
				case renderAxis of
				(
					#top:	topAxisTexFilenames =	asobo_planeSeatProjStruct.getAxisFilenames texFilePath texFileName texFileExtension #top	renderInfos	altTemp:keepTempMergeTextures	useTextureArrayFolder:useTextureArrayFolder
					#back:	backAxisTexFilenames =	asobo_planeSeatProjStruct.getAxisFilenames texFilePath texFileName texFileExtension #back	renderInfos	altTemp:keepTempMergeTextures	useTextureArrayFolder:useTextureArrayFolder
					#front:	frontAxisTexFilenames =	asobo_planeSeatProjStruct.getAxisFilenames texFilePath texFileName texFileExtension #front	renderInfos	altTemp:keepTempMergeTextures	useTextureArrayFolder:useTextureArrayFolder
					#side:	sideAxisTexFilenames =	asobo_planeSeatProjStruct.getAxisFilenames texFilePath texFileName texFileExtension #side	renderInfos	altTemp:keepTempMergeTextures	useTextureArrayFolder:useTextureArrayFolder
				)
			)
			
			local topAxisCombinedTexFilenames, backAxisCombinedTexFilenames, frontAxisCombinedTexFilenames, sideAxisCombinedTexFilenames
			for renderAxis in renderInfos.renderAxis do
			(
				case renderAxis of
				(
					#top:	topAxisCombinedTexFilenames =	asobo_planeSeatProjStruct.getAxisCombinedFilenames texFilePath texFileName texFileExtension #top	renderInfos	useTextureArrayFolder:useTextureArrayFolder
					#back:	backAxisCombinedTexFilenames =	asobo_planeSeatProjStruct.getAxisCombinedFilenames texFilePath texFileName texFileExtension #back	renderInfos	useTextureArrayFolder:useTextureArrayFolder
					#front:	frontAxisCombinedTexFilenames =	asobo_planeSeatProjStruct.getAxisCombinedFilenames texFilePath texFileName texFileExtension #front	renderInfos	useTextureArrayFolder:useTextureArrayFolder
					#side:	sideAxisCombinedTexFilenames =	asobo_planeSeatProjStruct.getAxisCombinedFilenames texFilePath texFileName texFileExtension #side	renderInfos	useTextureArrayFolder:useTextureArrayFolder
				)
			)
			
			local matchingFiles = #()
			for renderAxis in renderInfos.renderAxis do
			(
				case renderAxis of
				(
					#top:	asobo_planeSeatProjStruct.checkFileExists topAxisTexFilenames	&matchingFiles
					#back:	asobo_planeSeatProjStruct.checkFileExists backAxisTexFilenames	&matchingFiles
					#front:	asobo_planeSeatProjStruct.checkFileExists frontAxisTexFilenames	&matchingFiles
					#side:	asobo_planeSeatProjStruct.checkFileExists sideAxisTexFilenames	&matchingFiles
				)
			)
			for renderAxis in renderInfos.renderAxis do
			(
				case renderAxis of
				(
					#top:	asobo_planeSeatProjStruct.checkCombinedFileExists topAxisCombinedTexFilenames	&matchingFiles
					#back:	asobo_planeSeatProjStruct.checkCombinedFileExists backAxisCombinedTexFilenames	&matchingFiles
					#front:	asobo_planeSeatProjStruct.checkCombinedFileExists frontAxisCombinedTexFilenames	&matchingFiles
					#side:	asobo_planeSeatProjStruct.checkCombinedFileExists sideAxisCombinedTexFilenames	&matchingFiles
				)
			)
			local proceed = matchingFiles.count == 0
			if not proceed then
			(
				local extraInfos = ""
				for o in matchingFiles do extraInfos += "\n- " + o
				proceed = asobo_planeSeatProjStruct.qBox #fileOverwrite extraInfos:extraInfos
			)
			if proceed then
			(
				-- properly setup file save options
				local previousSaveOptions = asobo_planeSeatProjStruct.getSaveBitmapOptions()
				local fileFormat = asobo_planeSeatProjStruct.getAfterDotFilenameTypeName filename
				if forceBitmapSaveOptions then
				(
					if not (asobo_planeSeatProjStruct.setupSaveBitmapOptions type:fileFormat) then --only alter save options for used file format
					(
						asobo_planeSeatProjStruct.mBox #fileFormatSetupFail debugExtraTxt:(fileFormat as string)
						return false
					)
				)
				else
				(
					local safeUserSaveOptions = asobo_planeSeatProjStruct.setupMinimumSafeSaveBitmapOptions type:fileFormat
					if not (asobo_planeSeatProjStruct.setupSaveBitmapOptions saveOptions:safeUserSaveOptions type:fileFormat) then --only alter save options for used file format
					(
						asobo_planeSeatProjStruct.mBox #fileFormatSetupFail debugExtraTxt:(fileFormat as string)
						return false
					)
				)
				
				-- create textureArray directory and check directory exists
				for renderAxis in renderInfos.renderAxis do
				(
					local pn = case renderAxis of
					(
						#top:	asobo_planeSeatProjStruct.getName #top		allToLower:true
						#back:	asobo_planeSeatProjStruct.getName #back		allToLower:true
						#front:	asobo_planeSeatProjStruct.getName #front	allToLower:true
						#side:	asobo_planeSeatProjStruct.getName #side		allToLower:true
					)
					local folderFilename = if useTextureArrayFolder then (asobo_planeSeatProjStruct.getTextureArrayFolder (texFilePath + texFileName) suffix:pn) else texFilePath
					if not asobo_planeSeatProjStruct.isFolderCreated folderFilename then
					(
						asobo_planeSeatProjStruct.mBox #cantCreateFolder debugExtraTxt:(asobo_planeSeatProjStruct.getLastFolderName folderFilename)
						return false
					)
				)
				
				local progressDialog = asobo_planeSeatProjStruct.createProgressBar()
				
				asobo_planeSeatProjStruct.fixSceneState() -- make sure we are properly set
				
				-- lets keep scene ordered
				local projLayer = asobo_planeSeatProjStruct.createLayer()
				local projObjectsToDelete = #()
				
				-- get projection bounding box
				local selectionBBox = (asobo_planeSeatProjStruct()).boundingBox bBox:(asobo_planeSeatProjStruct.getSelectionBB validObjs)
				
				-- create and setup needed duplicates
				local renderObjs = asobo_planeSeatProjStruct.createRenderObjects validObjs selectionBBox renderInfos &progressDialog layer:projLayer
				if renderInfos.normal.active then
				(
					if not (renderInfos.normal.renderType == #projection and renderInfos.normal.projectionType == #default) then join projObjectsToDelete renderObjs.normal
				)
				if renderInfos.height.active then
				(
					if not (renderInfos.height.renderType == #projection and renderInfos.height.projectionType == #default) then
					(
						for renderAxis in renderInfos.renderAxis do
						(
							case renderAxis of
							(
								#top:	join projObjectsToDelete renderObjs.height.top
								#back:	join projObjectsToDelete renderObjs.height.back
								#front:	join projObjectsToDelete renderObjs.height.front
								#side:	join projObjectsToDelete renderObjs.height.side
							)
						)
					)
				)
				if renderInfos.ao.active then
				(
					if not (renderInfos.ao.renderType == #projection and renderInfos.ao.projectionType == #default) then join projObjectsToDelete renderObjs.ao
				)
				if renderInfos.emissive.active	then join projObjectsToDelete renderObjs.emissive
				if renderInfos.albedo.active	then join projObjectsToDelete renderObjs.albedo
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog 0.0 text:"Render setup" pauseOnUpdate:true
				
				local renderObjsPerAxis = (asobo_planeSeatProjStruct()).projectionObjectsPerAxis()
				local needHeightPerAxis = not (renderInfos.height.renderType == #projection and renderInfos.height.projectionType == #default) and renderInfos.height.active
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:
						(
							renderObjsPerAxis.top = (asobo_planeSeatProjStruct()).projectionObjects normal:renderObjs.normal ao:renderObjs.ao emissive:renderObjs.emissive albedo:renderObjs.albedo \
								height:(if needHeightPerAxis then renderObjs.height.top else renderObjs.height)
						)
						#back:
						(
							renderObjsPerAxis.back = (asobo_planeSeatProjStruct()).projectionObjects normal:renderObjs.normal ao:renderObjs.ao emissive:renderObjs.emissive albedo:renderObjs.albedo \
								height:(if needHeightPerAxis then renderObjs.height.back else renderObjs.height)
						)
						#front:
						(
							renderObjsPerAxis.front = (asobo_planeSeatProjStruct()).projectionObjects normal:renderObjs.normal ao:renderObjs.ao emissive:renderObjs.emissive albedo:renderObjs.albedo \
								height:(if needHeightPerAxis then renderObjs.height.front else renderObjs.height)
						)
						#side:
						(
							renderObjsPerAxis.side = (asobo_planeSeatProjStruct()).projectionObjects normal:renderObjs.normal ao:renderObjs.ao emissive:renderObjs.emissive albedo:renderObjs.albedo \
								height:(if needHeightPerAxis then renderObjs.height.side else renderObjs.height)
						)
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (1.0/10.0)
				
				-- get texture size for each plane
				local maxSideSizeAxis = asobo_planeSeatProjStruct.getMaxVectorAxis selectionBBox.bbSize
				local texSizeVector = case maxSideSizeAxis of
				(
					#X:	maxTextureSize * selectionBBox.bbSize / selectionBBox.bbSize.x
					#Y:	maxTextureSize * selectionBBox.bbSize / selectionBBox.bbSize.y
					#Z:	maxTextureSize * selectionBBox.bbSize / selectionBBox.bbSize.z
				)
				local safeTexSizeVector = asobo_planeSeatProjStruct.getSafeTextureSize texSizeVector dxtSafe:dxtSafe
				
				local topTexSize, backTexSize, frontTexSize, sideTexSize
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	topTexSize = [safeTexSizeVector.x, safeTexSizeVector.y]
						#back:	backTexSize = [safeTexSizeVector.x, safeTexSizeVector.z]
						#front:	frontTexSize = [safeTexSizeVector.x, safeTexSizeVector.z]
						#side:	sideTexSize = [safeTexSizeVector.y, safeTexSizeVector.z]
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (2.0/10.0)
				
				-- Bugfix
				local topBugNeedFix, backBugNeedFix, frontBugNeedFix, sideBugNeedFix
				local bugFixTopTexSize, bugFixBackTexSize, bugFixFrontTexSize, bugFixSideTexSize
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:
						(
							topBugNeedFix = topTexSize.x != topTexSize.y
							bugFixTopTexSize = if topBugNeedFix then [amax topTexSize.x topTexSize.y, amax topTexSize.x topTexSize.y] else topTexSize
						)
						#back:
						(
							backBugNeedFix = backTexSize.x != backTexSize.y
							bugFixBackTexSize = if backBugNeedFix then [amax backTexSize.x backTexSize.y, amax backTexSize.x backTexSize.y] else backTexSize
						)
						#front:
						(
							frontBugNeedFix = frontTexSize.x != frontTexSize.y
							bugFixFrontTexSize = if frontBugNeedFix then [amax frontTexSize.x frontTexSize.y, amax frontTexSize.x frontTexSize.y] else frontTexSize
						)
						#side:
						(
							sideBugNeedFix = sideTexSize.x != sideTexSize.y
							bugFixSideTexSize = if sideBugNeedFix then [amax sideTexSize.x sideTexSize.y, amax sideTexSize.x sideTexSize.y] else sideTexSize
						)
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (3.0/10.0)
				
				-- get projection bounding box with px margin
				local safeBBoxTexSize = asobo_planeSeatProjStruct.maxVector texSizeVector (pxMargin + 1) -- minimum texture size to compute safeBBox would be (pxMargin + 1)x(pxMargin + 1).
				local safeBBoxAmount = (((selectionBBox.bbSize * safeBBoxTexSize) / (safeBBoxTexSize - (pxMargin as float) * 2.0)) - selectionBBox.bbSize) / 2.0
				local selectionSafeBBox = (asobo_planeSeatProjStruct()).boundingBox bBox:(asobo_planeSeatProjStruct.safeBBox selectionBBox.bBox safeBBoxAmount)
					
				-- get proper axis for plane size - note that z axis is still used for heightmap
				local topSize, backSize, frontSize, sideSize
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:
						(
							local sizeX = if topBugNeedFix and topTexSize.x < topTexSize.y then selectionSafeBBox.bbSize.y else selectionSafeBBox.bbSize.x
							local sizeY = if topBugNeedFix and topTexSize.x > topTexSize.y then selectionSafeBBox.bbSize.x else selectionSafeBBox.bbSize.y
							topSize = [sizeX, sizeY, selectionBBox.bbSize.z]
						)
						#back:
						(
							local sizeX = if backBugNeedFix and backTexSize.x < backTexSize.y then selectionSafeBBox.bbSize.z else selectionSafeBBox.bbSize.x
							local sizeY = if backBugNeedFix and backTexSize.x > backTexSize.y then selectionSafeBBox.bbSize.x else selectionSafeBBox.bbSize.z
							backSize = [sizeX, sizeY, selectionBBox.bbSize.y]
						)
						#front:
						(
							local sizeX = if frontBugNeedFix and frontTexSize.x < frontTexSize.y then selectionSafeBBox.bbSize.z else selectionSafeBBox.bbSize.x
							local sizeY = if frontBugNeedFix and frontTexSize.x > frontTexSize.y then selectionSafeBBox.bbSize.x else selectionSafeBBox.bbSize.z
							frontSize = [sizeX, sizeY, selectionBBox.bbSize.y]
						)
						#side:
						(
							local sizeX = if sideBugNeedFix and sideTexSize.x < sideTexSize.y then selectionSafeBBox.bbSize.z else selectionSafeBBox.bbSize.y
							local sizeY = if sideBugNeedFix and sideTexSize.x > sideTexSize.y then selectionSafeBBox.bbSize.y else selectionSafeBBox.bbSize.z
							sideSize = [sizeX, sizeY, selectionBBox.bbSize.x]
						)
					)
				)
				
				local topPosition = 		[selectionBBox.bbCenter.x, selectionBBox.bbCenter.y, selectionBBox.bbMax.z]
				local topBackPosition = 	[selectionBBox.bbCenter.x, selectionBBox.bbCenter.y, selectionBBox.bbMin.z]
				local frontPosition = 		[selectionBBox.bbCenter.x, selectionBBox.bbMin.y, selectionBBox.bbCenter.z]
				local frontBackPosition = 	[selectionBBox.bbCenter.x, selectionBBox.bbMax.y, selectionBBox.bbCenter.z]
				local sidePosition = 		[selectionBBox.bbMin.x, selectionBBox.bbCenter.y, selectionBBox.bbCenter.z]
				local sideBackPosition = 	[selectionBBox.bbMax.x, selectionBBox.bbCenter.y, selectionBBox.bbCenter.z]
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (4.0/10.0)
				
				-- create projection planes
				-- need opposing plane for default heightmap and normal map to avoid ray misses
				local topBackPlanes, backBackPlanes, frontBackPlanes, sideBackPlanes
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:
						(
							topBackPlanes = asobo_planeSeatProjStruct.createProjectionBackPlanes topBackPosition #plusZ topSize renderInfos \
								name:(asobo_planeSeatProjStruct.getName #oppositeProjTopPlane) layer:projLayer
							if renderInfos.normal.active then	append projObjectsToDelete topBackPlanes.normal
							if renderInfos.height.active then	append projObjectsToDelete topBackPlanes.height
						)
						#back:
						(
							backBackPlanes = asobo_planeSeatProjStruct.createProjectionBackPlanes frontPosition #minusY backSize renderInfos \
								name:(asobo_planeSeatProjStruct.getName #oppositeProjBackPlane) layer:projLayer
							if renderInfos.normal.active then	append projObjectsToDelete backBackPlanes.normal
							if renderInfos.height.active then	append projObjectsToDelete backBackPlanes.height
						)
						#front:
						(
							frontBackPlanes = asobo_planeSeatProjStruct.createProjectionBackPlanes frontBackPosition #plusY frontSize renderInfos \
								name:(asobo_planeSeatProjStruct.getName #oppositeProjFrontPlane) layer:projLayer
							if renderInfos.normal.active then	append projObjectsToDelete frontBackPlanes.normal
							if renderInfos.height.active then	append projObjectsToDelete frontBackPlanes.height
						)
						#side:
						(
							sideBackPlanes = asobo_planeSeatProjStruct.createProjectionBackPlanes sideBackPosition #minusX sideSize renderInfos \
								name:(asobo_planeSeatProjStruct.getName #oppositeProjSidePlane) layer:projLayer
							if renderInfos.normal.active then	append projObjectsToDelete sideBackPlanes.normal
							if renderInfos.height.active then	append projObjectsToDelete sideBackPlanes.height
						)
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (5.0/10.0)
				
				local topPlanes, backPlanes, frontPlanes, sidePlanes
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:
						(
							topPlanes = asobo_planeSeatProjStruct.createProjectionPlanes topPosition #plusZ topSize topTexSize bugFixTopTexSize topAxisTexFilenames \
								renderObjsPerAxis.top topBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projTopPlane) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #projection		then append projObjectsToDelete topPlanes.normal.projPlane
							if renderInfos.height.active	and renderInfos.height.renderType == #projection		then append projObjectsToDelete topPlanes.height.projPlane
							if renderInfos.ao.active		and renderInfos.ao.renderType == #projection			then append projObjectsToDelete topPlanes.ao.projPlane
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #projection		then append projObjectsToDelete topPlanes.emissive.projPlane
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #projection		then append projObjectsToDelete topPlanes.albedo.projPlane
						)
						#back:
						(
							backPlanes = asobo_planeSeatProjStruct.createProjectionPlanes frontBackPosition #minusY backSize backTexSize bugFixBackTexSize backAxisTexFilenames \
								renderObjsPerAxis.back backBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projBackPlane) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #projection		then append projObjectsToDelete backPlanes.normal.projPlane
							if renderInfos.height.active	and renderInfos.height.renderType == #projection		then append projObjectsToDelete backPlanes.height.projPlane
							if renderInfos.ao.active		and renderInfos.ao.renderType == #projection			then append projObjectsToDelete backPlanes.ao.projPlane
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #projection		then append projObjectsToDelete backPlanes.emissive.projPlane
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #projection		then append projObjectsToDelete backPlanes.albedo.projPlane
						)
						#front:
						(
							frontPlanes = asobo_planeSeatProjStruct.createProjectionPlanes frontPosition #plusY frontSize frontTexSize bugFixFrontTexSize frontAxisTexFilenames \
								renderObjsPerAxis.front frontBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projFrontPlane) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #projection		then append projObjectsToDelete frontPlanes.normal.projPlane
							if renderInfos.height.active	and renderInfos.height.renderType == #projection		then append projObjectsToDelete frontPlanes.height.projPlane
							if renderInfos.ao.active		and renderInfos.ao.renderType == #projection			then append projObjectsToDelete frontPlanes.ao.projPlane
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #projection		then append projObjectsToDelete frontPlanes.emissive.projPlane
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #projection		then append projObjectsToDelete frontPlanes.albedo.projPlane
						)
						#side:
						(
							sidePlanes = asobo_planeSeatProjStruct.createProjectionPlanes sidePosition #minusX sideSize sideTexSize bugFixSideTexSize sideAxisTexFilenames \
								renderObjsPerAxis.side sideBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projSidePlane) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #projection		then append projObjectsToDelete sidePlanes.normal.projPlane
							if renderInfos.height.active	and renderInfos.height.renderType == #projection		then append projObjectsToDelete sidePlanes.height.projPlane
							if renderInfos.ao.active		and renderInfos.ao.renderType == #projection			then append projObjectsToDelete sidePlanes.ao.projPlane
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #projection		then append projObjectsToDelete sidePlanes.emissive.projPlane
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #projection		then append projObjectsToDelete sidePlanes.albedo.projPlane
						)
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (6.0/10.0)
				
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	asobo_planeSeatProjStruct.setupPlaneBakeMaps topPlanes renderInfos
						#back:	asobo_planeSeatProjStruct.setupPlaneBakeMaps backPlanes renderInfos
						#front:	asobo_planeSeatProjStruct.setupPlaneBakeMaps frontPlanes renderInfos
						#side:	asobo_planeSeatProjStruct.setupPlaneBakeMaps sidePlanes renderInfos
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (7.0/10.0)
				
				-- create projection cameras
				local topCameras, backCameras, frontCameras, sideCameras
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:
						(
							topCameras = asobo_planeSeatProjStruct.createFittingCameras topPosition #plusZ topSize topTexSize bugFixTopTexSize topAxisTexFilenames \
								renderObjsPerAxis.top topBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projTopCamera) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #camera		then append projObjectsToDelete topCameras.normal.projCamera
							if renderInfos.height.active	and renderInfos.height.renderType == #camera		then append projObjectsToDelete topCameras.height.projCamera
							if renderInfos.ao.active		and renderInfos.ao.renderType == #camera			then append projObjectsToDelete topCameras.ao.projCamera
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #camera		then append projObjectsToDelete topCameras.emissive.projCamera
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #camera		then append projObjectsToDelete topCameras.albedo.projCamera
						)
						#back:
						(
							backCameras = asobo_planeSeatProjStruct.createFittingCameras frontBackPosition #minusY backSize backTexSize bugFixBackTexSize backAxisTexFilenames \
								renderObjsPerAxis.back backBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projBackCamera) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #camera		then append projObjectsToDelete backCameras.normal.projCamera
							if renderInfos.height.active	and renderInfos.height.renderType == #camera		then append projObjectsToDelete backCameras.height.projCamera
							if renderInfos.ao.active		and renderInfos.ao.renderType == #camera			then append projObjectsToDelete backCameras.ao.projCamera
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #camera		then append projObjectsToDelete backCameras.emissive.projCamera
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #camera		then append projObjectsToDelete backCameras.albedo.projCamera
						)
						#front:
						(
							frontCameras = asobo_planeSeatProjStruct.createFittingCameras frontPosition #plusY frontSize frontTexSize bugFixFrontTexSize frontAxisTexFilenames \
								renderObjsPerAxis.front frontBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projFrontCamera) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #camera		then append projObjectsToDelete frontCameras.normal.projCamera
							if renderInfos.height.active	and renderInfos.height.renderType == #camera		then append projObjectsToDelete frontCameras.height.projCamera
							if renderInfos.ao.active		and renderInfos.ao.renderType == #camera			then append projObjectsToDelete frontCameras.ao.projCamera
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #camera		then append projObjectsToDelete frontCameras.emissive.projCamera
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #camera		then append projObjectsToDelete frontCameras.albedo.projCamera
						)
						#side:
						(
							sideCameras = asobo_planeSeatProjStruct.createFittingCameras sidePosition #minusX sideSize sideTexSize bugFixSideTexSize sideAxisTexFilenames \
								renderObjsPerAxis.side sideBackPlanes renderInfos name:(asobo_planeSeatProjStruct.getName #projSideCamera) layer:projLayer
							if renderInfos.normal.active	and renderInfos.normal.renderType == #camera		then append projObjectsToDelete sideCameras.normal.projCamera
							if renderInfos.height.active	and renderInfos.height.renderType == #camera		then append projObjectsToDelete sideCameras.height.projCamera
							if renderInfos.ao.active		and renderInfos.ao.renderType == #camera			then append projObjectsToDelete sideCameras.ao.projCamera
							if renderInfos.emissive.active	and renderInfos.emissive.renderType == #camera		then append projObjectsToDelete sideCameras.emissive.projCamera
							if renderInfos.albedo.active	and renderInfos.albedo.renderType == #camera		then append projObjectsToDelete sideCameras.albedo.projCamera
						)
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (8.0/10.0)
				
				-- render!
				-- note: Arnold crashes if trying to render portrait images! lol 3dsmax.. RenderToTexture doesn't make it crash but rendered images gets cropped if height > width
				-- note2: Scanline renderer gives crappy results when rendering to texture
				-- note3: projection will not work properly with scanline if not square output...
				-- note4: rendering projection with scanline will break render -> need to render THEN crop
				local previousRenderer = renderers.current
				local previousFileInGamma = fileInGamma
				local previousFileOutGamma = fileOutGamma
				local currentSceneExposureControl = SceneExposureControl.exposureControl
				local previousSceneExposureControlActive = if currentSceneExposureControl != undefined then currentSceneExposureControl.active else false
				
				-- disable exposure control
				if previousSceneExposureControlActive then currentSceneExposureControl.active = false
				
	-- 			renderers.current = Default_Scanline_Renderer()
	-- 			renderers.current = Arnold()
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (9.0/10.0)
				
				-- is renderer switching slowing down render? -> split renders per renderer...
				-- seems like starting with scanline and then switching to arnold is the fastest way to go
				local topPlanesArnold, backPlanesArnold, frontPlanesArnold, sidePlanesArnold
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	topPlanesArnold = asobo_planeSeatProjStruct.filterPlanesByRendererType topPlanes renderInfos #arnold
						#back:	backPlanesArnold = asobo_planeSeatProjStruct.filterPlanesByRendererType backPlanes renderInfos #arnold
						#front:	frontPlanesArnold = asobo_planeSeatProjStruct.filterPlanesByRendererType frontPlanes renderInfos #arnold
						#side:	sidePlanesArnold = asobo_planeSeatProjStruct.filterPlanesByRendererType sidePlanes renderInfos #arnold
					)
				)
				local topPlanesScanline, backPlanesScanline, frontPlanesScanline, sidePlanesScanline
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	topPlanesScanline = asobo_planeSeatProjStruct.filterPlanesByRendererType topPlanes renderInfos #scanline
						#back:	backPlanesScanline = asobo_planeSeatProjStruct.filterPlanesByRendererType backPlanes renderInfos #scanline
						#front:	frontPlanesScanline = asobo_planeSeatProjStruct.filterPlanesByRendererType frontPlanes renderInfos #scanline
						#side:	sidePlanesScanline = asobo_planeSeatProjStruct.filterPlanesByRendererType sidePlanes renderInfos #scanline
					)
				)
				local topCamerasArnold, backCamerasArnold, frontCamerasArnold, sideCamerasArnold
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	topCamerasArnold = asobo_planeSeatProjStruct.filterCamerasByRendererType topCameras renderInfos #arnold
						#back:	backCamerasArnold = asobo_planeSeatProjStruct.filterCamerasByRendererType backCameras renderInfos #arnold
						#front:	frontCamerasArnold = asobo_planeSeatProjStruct.filterCamerasByRendererType frontCameras renderInfos #arnold
						#side:	sideCamerasArnold = asobo_planeSeatProjStruct.filterCamerasByRendererType sideCameras renderInfos #arnold
					)
				)
				local topCamerasScanline, backCamerasScanline, frontCamerasScanline, sideCamerasScanline
				for renderAxis in renderInfos.renderAxis do
				(
					case renderAxis of
					(
						#top:	topCamerasScanline = asobo_planeSeatProjStruct.filterCamerasByRendererType topCameras renderInfos #scanline
						#back:	backCamerasScanline = asobo_planeSeatProjStruct.filterCamerasByRendererType backCameras renderInfos #scanline
						#front:	frontCamerasScanline = asobo_planeSeatProjStruct.filterCamerasByRendererType frontCameras renderInfos #scanline
						#side:	sideCamerasScanline = asobo_planeSeatProjStruct.filterCamerasByRendererType sideCameras renderInfos #scanline
					)
				)
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog (10.0/10.0)
				
				local renderWasCancelled = false
				for i = 1 to renderInfos.renderAxis.count while not renderWasCancelled do
				(
					case renderInfos.renderAxis[i] of
					(
						#top:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projTopPlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps topPlanesScanline topCamerasScanline previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
						#back:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projBackPlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps backPlanesScanline backCamerasScanline previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
						#front:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projFrontPlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps frontPlanesScanline frontCamerasScanline previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
						#side:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projSidePlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps sidePlanesScanline sideCamerasScanline previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
					)
				)
				for i = 1 to renderInfos.renderAxis.count while not renderWasCancelled do
				(
					case renderInfos.renderAxis[i] of
					(
						#top:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projTopPlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps topPlanesArnold topCamerasArnold previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
						#back:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projBackPlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps backPlanesArnold backCamerasArnold previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
						#front:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projFrontPlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps frontPlanesArnold frontCamerasArnold previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
						#side:
						(
							asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float) text:("rendering " + (asobo_planeSeatProjStruct.getName #projSidePlane)) pauseOnUpdate:true
							asobo_planeSeatProjStruct.renderMaps sidePlanesArnold sideCamerasArnold previousFileInGamma previousFileOutGamma &renderWasCancelled showRendering:showRendering
						)
					)
				)
				
				-- reset renderer
				renderers.current = previousRenderer
				-- reset selection after baking
				select objs
				-- delete objects + layer needed only for projection render
				delete projObjectsToDelete
				asobo_planeSeatProjStruct.deleteLayer projLayer
				
				-- bitmap manipulations
				if not renderWasCancelled and mergeTexturesPhaseActive then
				(
					asobo_planeSeatProjStruct.updateProgressBar progressDialog 0.0 text:"Merging rendered maps"
					for i = 1 to renderInfos.renderAxis.count do
					(
						asobo_planeSeatProjStruct.updateProgressBar progressDialog (i as float / (renderInfos.renderAxis.count + 1) as float)
						case renderInfos.renderAxis[i] of
						(
							#top:(
								asobo_planeSeatProjStruct.createCombinedMaps topAxisTexFilenames topAxisCombinedTexFilenames activeMergeTextures
							)
							#back:(
								asobo_planeSeatProjStruct.createCombinedMaps backAxisTexFilenames backAxisCombinedTexFilenames activeMergeTextures
							)
							#front:(
								asobo_planeSeatProjStruct.createCombinedMaps frontAxisTexFilenames frontAxisCombinedTexFilenames activeMergeTextures
							)
							#side:(
								asobo_planeSeatProjStruct.createCombinedMaps sideAxisTexFilenames sideAxisCombinedTexFilenames activeMergeTextures
							)
						)
					)
					if not keepTempMergeTextures then
					(
						for renderAxis in renderInfos.renderAxis do
						(
							case renderAxis of
							(
								#top:	asobo_planeSeatProjStruct.deleteAxisTempFiles topAxisTexFilenames tempTextures
								#back:	asobo_planeSeatProjStruct.deleteAxisTempFiles backAxisTexFilenames tempTextures
								#front:	asobo_planeSeatProjStruct.deleteAxisTempFiles frontAxisTexFilenames tempTextures
								#side:	asobo_planeSeatProjStruct.deleteAxisTempFiles sideAxisTexFilenames tempTextures
							)
						)
					)
				)
				
				-- reset bitmapSaveOptions
				setupSaveBitmapOptions saveOptions:previousSaveOptions type:fileFormat
				
				-- reset gamma
				fileInGamma = previousFileInGamma
				fileOutGamma = previousFileOutGamma
				-- reset exposure control
				if previousSceneExposureControlActive then currentSceneExposureControl.active = true
				
				asobo_planeSeatProjStruct.updateProgressBar progressDialog 1.0 text:(if renderWasCancelled then "Canceled!" else "Finished!") pauseOnUpdate:true
				
				-- delete progress bar
				asobo_planeSeatProjStruct.deleteProgressBar progressDialog
				asobo_planeSeatProjStruct.mBox (if renderWasCancelled then #projectionCancelled else #projectionComplete)
			) -- no matching file found or overwrite allowed
		) -- at least one object to process
	)
)

macroScript asobo_planeSeatProj
category:"ASOBO"
buttonText:"Seat projection"
icon:#("Standard_Modifiers",19)
toolTip:"Create seat projection textures"
silentErrors:false
autoUndoEnabled:false
(
	/* Rollout toggle behavior" */
	local isOpen = false
	
	
	local uiWidth = 515
	local uiLeftWidth = 340
	local uiRightWidth = uiWidth - uiLeftWidth
	local uiTopHeight = 270
	local btnOffset = -22-(floor uiRightWidth/6.0)
	local btnWidth = 28
	
	rollout planeSeatProjRollout "Seat projection"
	(
		-- some hardcoded options
		local dxtSafe = true
		local defaultFileExt = "tif"
		
		-- bitmapSaveOptionsBehavior
		local bitmapSaveOptions
		local forceBitmapSaveOptions = false
		-- texture margin behavior
		local texMargin1024
		
		groupbox grpProjTex "Projection textures" width:uiLeftWidth height:uiTopHeight align:#left offset:[-8,0]
			edittext txtFilePath "File path:" text:"" fieldwidth:180 align:#right offset:[-34-uiRightWidth,-uiTopHeight+15]
			edittext txtFilename "File name and type:" text:("projectionTexture."+defaultFileExt) fieldwidth:180 align:#right offset:[-34-uiRightWidth,0]
			button btnChooseFilename "..." tooltip:("Select where to save textures\n(Right click for advanced "+defaultFileExt+" options)") align:#right width:37 height:40 offset:[6-uiRightWidth,-45]
			label lbFinalNames "Final texture names: (" align:#left across:2
			checkbox createTexArraySubFolder "Create texture array subfolder)" tooltip:"Projection uses texture arrays and need subfolder to work properly" checked:true offset:[-140,0]
-- 			label lbFinalNamesInfo "(xxx is axis: top, side, etc..)" align:#left enabled:false visible:false offset:[50-(uiLeftWidth/2.0),0]
			label lbFinalNamesPath "" align:#left enabled:false visible:false offset:[10,0]
			label lbFinalName1 "" align:#left enabled:false offset:[20,0]
			label lbFinalName2 "" align:#left enabled:false offset:[20,0]
			label lbFinalName3 "" align:#left enabled:false offset:[20,0]
			label lbFinalName4 "" align:#left enabled:false offset:[20,0]
			label lbFinalName5 "" align:#left enabled:false offset:[20,0]
			spinner spMaxTexSize "Max texture size (px):" tooltip:"Maximum texture size (pixels)" range:[(if dxtSafe then 4 else 1), 1048576, 1024] type:#integer scale:1 fieldWidth:50 align:#left offset:[0,5] across:2
			spinner spTexMargin "Margin (px):" tooltip:"Margin around rendered objects (pixels)" range:[0, 524287, 8] type:#integer scale:1 fieldWidth:50 align:#right offset:[0-uiRightWidth,5]
			button btnTexMaxSize128 "128" tooltip:"set texture max size to 128px" width:btnWidth align:#left across:6 offset:[btnOffset*0,0]
			button btnTexMaxSize256 "256" tooltip:"set texture max size to 256px" width:btnWidth align:#left offset:[btnOffset*1,0]
			button btnTexMaxSize512 "512" tooltip:"set texture max size to 512px" width:btnWidth align:#left offset:[btnOffset*2,0]
			button btnTexMaxSize1024 "1024" tooltip:"set texture max size to 1024px" width:btnWidth align:#left offset:[btnOffset*3,0]
			button btnTexMaxSize2048 "2048" tooltip:"set texture max size to 2048px" width:btnWidth align:#left offset:[btnOffset*4,0]
			button btnTexMaxSize4096 "4096" tooltip:"set texture max size to 4096px" width:btnWidth align:#left offset:[btnOffset*5,0]
			checkbox chkCreateMaterial "Create material" tooltip:"Create new material using baked projection" checked:false offset:[0,5] enabled:false --TODO!
		
		groupbox grpAdvancedOptions "Advanced options" width:(uiRightWidth - 14) height:(uiTopHeight+30) align:#right offset:[8, -uiTopHeight+3]
			groupbox grpProj "Projection" width:(uiRightWidth - 14 - 8) height:105 align:#left offset:[uiLeftWidth,-(uiTopHeight+30)+15]
				checkbox chkProjSide "Side (mandatory)" tooltip:"Render side projection textures" checked:true offset:[10+uiLeftWidth,-105+15]
				checkbox chkProjFront "Front" tooltip:"Render front projection textures" checked:false offset:[10+uiLeftWidth,0]
				checkbox chkProjBack "Back" tooltip:"Render back projection textures" checked:false offset:[10+uiLeftWidth,0]
				checkbox chkProjTop "Top" tooltip:"Render top projection textures" checked:false offset:[10+uiLeftWidth,0]
			groupbox grpTex "Textures" width:(uiRightWidth - 14 - 8) height:165 align:#left offset:[uiLeftWidth,10]
				checkbox chkAlbedo "Albedo" tooltip:"Render albedo textures" checked:true offset:[10+uiLeftWidth,-165+15]
				checkbox chkHeight "Height" tooltip:"Render height textures" checked:true offset:[10+uiLeftWidth,0]
				checkbox chkNormal "Normal" tooltip:"Render normal textures" checked:true offset:[10+uiLeftWidth,5]
				checkbox chkAO "AO" tooltip:"Render ambient occlusion textures" checked:true offset:[10+uiLeftWidth,0]
				checkbox chkEmissive "Emissive" tooltip:"Render emissive textures" checked:false offset:[10+uiLeftWidth,5]
				label lbMergeAlbedoHeight "}" align:#left offset:[75+uiLeftWidth,-98] enabled:false across:2
				checkbox chkMergeAlbedoHeight "Merge" tooltip:"Merge Albedo + Height together" align:#left checked:true offset:[uiLeftWidth-160,-98]
				label lbMergeNormalAO "}" align:#left offset:[75+uiLeftWidth,23] enabled:false across:2
				checkbox chkMergeNormalAO "Merge" tooltip:"Merge Normal + AO together" align:#left checked:true offset:[uiLeftWidth-160,23]
				label lbSeparator "________________" align:#left offset:[(uiRightWidth/2.0)+uiLeftWidth-55,30] enabled:false
				checkbox chkKeepMergeWorkingCopies "Keep merge work copies" tooltip:"Keep working copies of textures used for merge" checked:false offset:[10+uiLeftWidth,0]
		
		button btnCreateSeatProjTextures "Create projection textures" tooltip:"Create projection textures for selected object(s)" align:#left width:150 height:25 pos:[-75+uiLeftWidth/2.0,uiTopHeight+10]
		checkbox chkShowRendering "Show render" tooltip:"Display rendering window while baking" checked:false align:#left pos:[80+uiLeftWidth/2.0, uiTopHeight+15]
		
		fn albedoHeightChecked = chkAlbedo.checked and chkHeight.checked
		fn normalAoChecked = chkNormal.checked and chkAO.checked
		fn albedoHeightMerge = albedoHeightChecked() and chkMergeAlbedoHeight.checked
		fn normalAoMerge = normalAoChecked() and chkMergeNormalAO.checked
		fn isMergeActive =	albedoHeightMerge() or normalAoMerge()
		fn setMergeBtnsState =
		(
			lbMergeAlbedoHeight.visible = albedoHeightChecked()
			chkMergeAlbedoHeight.visible = albedoHeightChecked()
			lbMergeNormalAO.visible = chkNormal.checked and chkAO.checked
			chkMergeNormalAO.visible = chkNormal.checked and chkAO.checked
		)
		fn setKeepMergeCopiesState = chkKeepMergeWorkingCopies.enabled = isMergeActive()
		
		fn updateTexMarginValue texSize =
		(
			spTexMargin.value = (asobo_planeSeatProjStruct.roundNb (texSize * texMargin1024 / 1000.0) afterComma:0) as integer
		)
		fn updateTexMargin1024Value marginValue =
		(
			texMargin1024 = 1000.0 * marginValue / spMaxTexSize.value --multiplied by 1000 for more precision
		)
		on spTexMargin changed val do updateTexMargin1024Value val
		on spMaxTexSize changed val do updateTexMarginValue val
		
		fn setTexMaxSizeValue v =
		(
			spMaxTexSize.value = v
			updateTexMarginValue v
		)
		on btnTexMaxSize128 pressed do setTexMaxSizeValue 128
		on btnTexMaxSize256 pressed do setTexMaxSizeValue 256
		on btnTexMaxSize512 pressed do setTexMaxSizeValue 512
		on btnTexMaxSize1024 pressed do setTexMaxSizeValue 1024
		on btnTexMaxSize2048 pressed do setTexMaxSizeValue 2048
		on btnTexMaxSize4096 pressed do setTexMaxSizeValue 4096
		
		fn isEmptyPath =
		(
			(trimleft (trimright txtFilePath.text " ") " ") == ""
		)
		fn getCleanFilePath =
		(
			asobo_planeSeatProjStruct.addFilePathEndSlash (asobo_planeSeatProjStruct.fixFilePath txtFilePath.text)
		)
		fn getFullFilePathAndName =
		(
			local filePath = getCleanFilePath()
			local fileName = txtFilename.text
			filePath + fileName
		)
		
		fn updateFinalNames =
		(
			local fullFilePathAndName = getFullFilePathAndName()
			local fillLines = #()
			local labels = #(lbFinalName1, lbFinalName2, lbFinalName3, lbFinalName4, lbFinalName5)
			local validFiles = false
			if not isEmptyPath() and asobo_planeSeatProjStruct.checkFilePath fullFilePathAndName then
			(
				if asobo_planeSeatProjStruct.checkFileName fullFilePathAndName then
				(
					if chkProjSide.checked or chkProjFront.checked or chkProjBack.checked or chkProjTop.checked then
					(
						local texFileName = getFilenameFile fullFilePathAndName
						local texFileExtension = getFilenameType fullFilePathAndName
						local mergeAlbedoHeight = chkAlbedo.checked and chkHeight.checked and chkMergeAlbedoHeight.checked
						local mergeNormalAo = chkNormal.checked and chkAO.checked and chkMergeNormalAO.checked
						local dNames = #()
						local dPath = ""
						local axisName = ""
						local multipleAxisDisplay = false
						if chkProjSide.checked then
						(
							axisName += "side"
							if chkProjFront.checked or chkProjBack.checked or chkProjTop.checked then axisName += ","
						)
						if chkProjFront.checked then
						(
							axisName += " front"
							if chkProjBack.checked or chkProjTop.checked then axisName += ","
						)
						if chkProjBack.checked then
						(
							axisName += " back"
							if chkProjTop.checked then axisName += ","
						)
						if chkProjTop.checked then axisName += " top"
						if axisName[1] == " " then axisName = substring axisName 2 axisName.count
						if (for o in #(chkProjSide.checked, chkProjFront.checked, chkProjBack.checked, chkProjTop.checked) where o collect o).count > 1 then axisName = "[" + axisName + "]"
						if mergeAlbedoHeight		then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #albedoHeightMap	suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
						else
						(
							if chkAlbedo.checked	then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #albedoMap		suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
							if chkHeight.checked	then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #heightMap		suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
						)
						if mergeNormalAo			then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #normalAoMap		suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
						else
						(
							if chkNormal.checked	then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #normalMap		suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
							if chkAO.checked		then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #aoMap			suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
						)
						if chkEmissive.checked		then append dNames (asobo_planeSeatProjStruct.createFileName texFileName texFileExtension #emissiveMap		suffix:axisName	useTextureArrayFolder:createTexArraySubFolder.checked)
						
						if dNames.count > 0 then
						(
							dPath = getFilenamePath dNames[1]
							validFiles = true
							fillLines = for o in dNames collect filenameFromPath o
						)
						else
						(
							fillLines = #(	"please select at least",
											"one texture to render")
						)
						
-- 						local finalNamesInfo = "(xxx is axis:"finalNamesInfo += ")"
						lbFinalNamesPath.text = dPath
-- 						lbFinalNamesInfo.text = finalNamesInfo
					)
					else
					(
						fillLines = #(	"please select at least",
										"one projection axis to render")
					)
				)
				else
				(
					fillLines = #(	"please fix file name",
									"to see final texture names",
									"(need: name.extension)")
				)
			)
			else
			(
				fillLines = #(	"please choose save path",
								"to see final texture names")
			)
			--fill labels up in UI
			--if not valid put everything centered down in contrast
			local startFillPos = if validFiles then
			(
				0
-- 				labels.count - fillLines.count
			)
			else
			(
				ceil((labels.count - fillLines.count) / 2.0) --(floor: shift up if even number, ceil shift down)
			)
			local fillID = 1
			for i = 1 to labels.count do
			(
				if i <= startFillPos or fillID > fillLines.count then labels[i].text = ""
				else
				(
					labels[i].text = fillLines[fillID]
					fillID += 1
				)
			)
			--lbFinalNamesInfo.visible = validFiles
			lbFinalNamesPath.visible = validFiles
		)
		
		on txtFilePath changed txt do
		(
			updateFinalNames()
		)
		on txtFilename changed txt do
		(
			updateFinalNames()
		)
		
		fn disableAllProjBut but =
		(
			local allProj = #(chkProjSide, chkProjFront, chkProjBack, chkProjTop)
			if but.checked and (for o in allProj where o != but and o.checked collect o).count == 0 then
			(
				for o in allProj do o.checked = true
			)
			else
			(
				for o in allProj where o != but do o.checked = false
				but.checked = true
			)
			updateFinalNames()
			setMergeBtnsState()
			setKeepMergeCopiesState()
		)
		on chkProjSide	rightClick do disableAllProjBut chkProjSide
		on chkProjFront	rightClick do disableAllProjBut chkProjFront
		on chkProjBack	rightClick do disableAllProjBut chkProjBack
		on chkProjTop	rightClick do disableAllProjBut chkProjTop
		
		fn disableAllMapsBut but =
		(
			local allMaps = #(chkAlbedo, chkHeight, chkNormal, chkAO, chkEmissive)
			if but.checked and (for o in allMaps where o != but and o.checked collect o).count == 0 then
			(
				for o in allMaps do o.checked = true
			)
			else
			(
				for o in allMaps where o != but do o.checked = false
				but.checked = true
			)
			updateFinalNames()
			setMergeBtnsState()
			setKeepMergeCopiesState()
		)
		on chkAlbedo	rightClick do disableAllMapsBut chkAlbedo
		on chkHeight	rightClick do disableAllMapsBut chkHeight
		on chkNormal	rightClick do disableAllMapsBut chkNormal
		on chkAO		rightClick do disableAllMapsBut chkAO
		on chkEmissive	rightClick do disableAllMapsBut chkEmissive
		
		on createTexArraySubFolder	changed state do updateFinalNames()
		on chkProjSide				changed state do updateFinalNames()
		on chkProjFront				changed state do updateFinalNames()
		on chkProjBack				changed state do updateFinalNames()
		on chkProjTop				changed state do updateFinalNames()
		
		on chkAlbedo				changed state do (updateFinalNames(); setMergeBtnsState(); setKeepMergeCopiesState())
		on chkHeight				changed state do (updateFinalNames(); setMergeBtnsState(); setKeepMergeCopiesState())
		on chkNormal				changed state do (updateFinalNames(); setMergeBtnsState(); setKeepMergeCopiesState())
		on chkAO					changed state do (updateFinalNames(); setMergeBtnsState(); setKeepMergeCopiesState())
		on chkEmissive				changed state do updateFinalNames()
		
		on chkMergeAlbedoHeight		changed state do (updateFinalNames(); setKeepMergeCopiesState())
		on chkMergeNormalAO			changed state do (updateFinalNames(); setKeepMergeCopiesState())
		
		fn chooseSavePath type =
		(
			local seed = getFullFilePathAndName()
			if isEmptyPath() or not asobo_planeSeatProjStruct.checkFilePath seed then
			(
				-- no path, add default path
				seed = asobo_planeSeatProjStruct.getSaveHistory() + seed
			)
			local f = case type of
			(
				#leftClick:
				(
					forceBitmapSaveOptions = true
					asobo_planeSeatProjStruct.chooseSavePath filename:seed
				)
				#rightClick:
				(
					asobo_planeSeatProjStruct.chooseSaveBitmap &forceBitmapSaveOptions filename:seed --allow user to set file format options as desired, and fallback to forced format dialog if noob detected
				)
			)
			if f != undefined then
			(
				bitmapSaveOptions = asobo_planeSeatProjStruct.getSaveBitmapOptions()
				txtFilePath.text = getFilenamePath f
				txtFilename.text = filenameFromPath f
				updateFinalNames()
			)
		)
		on btnChooseFilename pressed do chooseSavePath #leftClick
		on btnChooseFilename rightclick do chooseSavePath #rightClick -- secret advanced user dialog, allow for file format custom setup (metadata, premultiplied alpha...) setup
		
		on btnCreateSeatProjTextures pressed do
		(
			local renderAxis = #()
			if chkProjTop.checked then append renderAxis #top
			if chkProjBack.checked then append renderAxis #back
			if chkProjFront.checked then append renderAxis #front
			if chkProjSide.checked then append renderAxis #side
			if renderAxis.count == 0 then
			(
				asobo_planeSeatProjStruct.mBox #noRenderAxis
			)
			else
			(
				local renderTextures = #()
				if chkNormal.checked then append renderTextures #normalMap
				if chkHeight.checked then append renderTextures #heightMap
				if chkAO.checked then append renderTextures #aoMap
				if chkEmissive.checked then append renderTextures #emissiveMap
				if chkAlbedo.checked then append renderTextures #albedoMap
				if renderTextures.count == 0 then
				(
					asobo_planeSeatProjStruct.mBox #noRenderTexture
				)
				else
				(
					local fullFilePathAndName = getFullFilePathAndName()
					if not isEmptyPath() and asobo_planeSeatProjStruct.checkFilePath fullFilePathAndName then
					(
						if asobo_planeSeatProjStruct.checkFileName fullFilePathAndName then
						(
							-- check if user save options have changed while UI was opened
							if not forceBitmapSaveOptions then
							(
								forceBitmapSaveOptions = not asobo_planeSeatProjStruct.compareSaveBitmapOptions bitmapSaveOptions type:(asobo_planeSeatProjStruct.getAfterDotFilenameTypeName fullFilePathAndName)
							)
							local mergeTextures = #()
							if albedoHeightMerge() then append mergeTextures #albedoHeightMap
							if normalAoMerge() then append mergeTextures #normalAoMap
							asobo_planeSeatProjStruct.getModelProjTextures \
								renderAxis:renderAxis \
								renderTextures:renderTextures \
								mergeTextures:mergeTextures \
								filename:fullFilePathAndName \
								useTextureArrayFolder:createTexArraySubFolder.checked \
								forceBitmapSaveOptions:forceBitmapSaveOptions \
								keepTempMergeTextures:chkKeepMergeWorkingCopies.checked \
								maxTextureSize:spMaxTexSize.value \
								pxMargin:spTexMargin.value \
								dxtSafe:dxtSafe \
								showRendering:chkShowRendering.checked
						)
						else asobo_planeSeatProjStruct.mBox #noValidSaveFile
					)
					else asobo_planeSeatProjStruct.mBox #noValidSavePath
				)--noRenderTexture
			)--noRenderAxis
		)
		
		on planeSeatProjRollout open do
		(
			updateFinalNames()
			updateTexMargin1024Value spTexMargin.value
		)
		/* Rollout toggle behavior" */
		on planeSeatProjRollout close do
		(
			isOpen = false
			updateToolbarButtons()
		)
	)
	
	/* Rollout toggle behavior" */
	on isChecked return isOpen
	on execute do
	(
		if isOpen then
		(
			destroyDialog planeSeatProjRollout
			isOpen = false
		)
		else 
		(
			createDialog planeSeatProjRollout width:uiWidth
			isOpen = true
		)
	)
	on closeDialogs do destroyDialog planeSeatProjRollout
)
