-- rev date: 12/02/2019
-- this script supports at least 3ds Max 2016 and later. Should support earlier versions but is untested in those versions.
-- this script removes NoteTracks from Max MotionClip Manager in Track View.
-- this script removes unused Clip Associations from Max MotionClip Manager in Track View.
-- this script removes Anim Layers from Anim Layer Control Manager
-- 09/10/19: add bad_notetrack_key_content2
-- 12/02/19: fixed bug when have used clip associations
-- 7/29/23: fixed logic on when to delete Anim Layers

struct cleanScene_def
(
private
	
	-- these are options that can be enabled/disabled......
	
	-- default value on whether to check value of note track keys to ensure they contain known garbage value. If checked, all keys in note
	-- track must contain the garbage value before the note track is deleted. Slow, but safe
	perform_notetrack_key_value_check_default = true,
	
	-- whether the check all trackview nodes for note tracks abd delete those found. 
	-- If set to true, need to uncomment "TrackviewNodes Note Tracks" in MaxSceneCleaning_ro
	perform_trackview_node_notetrack_check = false,

	-- whether to close the dialog when done
	close_dialog_when_done = true,
	
	-- end of options
	
	-- the garbage value held by Max MotionClip Manager notetrack keys
	bad_notetrack_key_content = "\x130\n",
	bad_notetrack_key_content2 = "\x49\n",

	MaxSceneCleaning_ro = rollout MaxSceneCleaning_ro "Max Scene Cleaning" width:350
	(
		group "Max MotionClip Manager"
		(
			label l1_a "Number of NoteTracks:" across:2 align:#left
			label l1_b "0" align:#right
			label l2_a "Processing NoteTrack:" across:2 align:#left
			label l2_b "0" align:#right
			label l3_a "Number of NoteTrack keys:" across:2 align:#left
			label l3_b "0" align:#right
			label l4_a "Number of NoteTracks deleted:" across:2 align:#left
			label l4_b "0" align:#right
			checkbutton cb_key_check "Check key values" checked:true
			label l5_a "Number of Clip Associations:" across:2 align:#left
			label l5_b "0" align:#right
			label l6_a "Processing Clip Association:" across:2 align:#left
			label l6_b "0" align:#right
			label l7_a "Number of Clip Associations deleted:" across:2 align:#left
			label l7_b "0" align:#right
		)
		group "Anim Layer Control Manager Layers"
		(
			label l8_a "Number of Anim Layers in Anim Layer Control Manager:" across:2 align:#left
			label l8_b "0" align:#right
			label l9_a "Number of Anim Layers deleted:" across:2 align:#left
			label l9_b "0" align:#right
		)
		
/*		group "TrackviewNodes Note Tracks"
		(
			label l11_a "Number of Note Tracks under 'trackViewNodes':" across:2 align:#left
			label l11_b "unknown" align:#right
			label l12_a "Number of Note Tracks deleted:" across:2 align:#left
			label l12_b "0" align:#right
		)
*/		
		checkbutton cb_abort "Abort"
	),

	-- function to recursively count the number of note tracks under a tvnode
	-- found will contain datapairs of path of tvnode and number of note tracks on tvnode when number is not zero
	fn countNoteTracksRecursive tvnode path found:#() =
	(
		windows.processpostedmessages()
		if MaxSceneCleaning_ro.cb_abort.checked do 
			return 0
		local count = 0
		if (tvnode != undefined) do
		(
			count = numNoteTracks tvnode
			if count != 0 do
			(
				format "path: %; # note tracks: %\n" path count
				append found (datapair path count)
			)
			path = path + "." + tvnode.name
			for i = 1 to tvnode.numsubs do
			(
				count += (countNoteTracksRecursive (tvnode[i]) path found:found)
				if MaxSceneCleaning_ro.cb_abort.checked do 
					return 0
			)
		)
		count -- return value
	),
		
	-- function to count the number of note tracks under 'trackViewNodes'
	-- found will contain datapairs of path of tvnode and number of note tracks on tvnode when number is not zero
	fn countTVNoteTracks found:#() =
	(
		local count = 0
		for trackIndex = 1 to trackViewNodes.numsubs do
		(
			local tvnode = trackViewNodes[trackIndex]
			count += (countNoteTracksRecursive tvnode tvnode.name found:found)
			if MaxSceneCleaning_ro.cb_abort.checked do 
				return 0
		)
		count -- return value
	),
	
	-- function to recursively delete the note tracks under a tvnode
	fn cleanNoteTracksRecursive tvnode cum_count =
	(
		if (tvnode != undefined) do
		(
			local count = numNoteTracks tvnode
			if count != 0 do
			(
				for i = 1 to count do
				(
					local tr = getNoteTrack tvnode (count - i + 1)
					deleteNoteTrack tvnode tr
					cum_count += 1
					MaxSceneCleaning_ro.l12_b.text = cum_count as string
				)
			)
			for i = 1 to tvnode.numsubs do
			(
				cum_count = (cleanNoteTracksRecursive (tvnode[i]) cum_count)
			)
		)
		cum_count -- return value
	),
	
	-- function to delete the note tracks under 'trackViewNodes'
	fn cleanTVNoteTracks =
	(
		local cum_count = 0
		for trackIndex = 1 to trackViewNodes.numsubs do
		(
			local tvnode = trackViewNodes[trackIndex]
			cum_count = (cleanNoteTracksRecursive tvnode cum_count)
		)
		cum_count
	),

	fn MaybeDeleteAnimLayer AnimLayers index =
	(
		-- the anim layer can be deleted if it contains no layer controllers
		local okToDelete = true
		local animLayer = AnimLayers[index]
		local nrefs = refs.getnumrefs animLayer
		for j = 2 to nrefs while okToDelete do  -- ref 1 is pb
		(
			local ref = refs.getreference animLayer j
			okToDelete =  ref == undefined or (classof ref == NodeMonitor)
		)
		if okToDelete do
		(
			AnimLayerManager.deleteLayer index
		)
		return okToDelete
	),

public
	fn cleanScene =
	(
		-------------------------
		createdialog MaxSceneCleaning_ro
		
		if not perform_trackview_node_notetrack_check and isproperty MaxSceneCleaning_ro #l11_a do
		(
			MaxSceneCleaning_ro.l11_a.enabled = MaxSceneCleaning_ro.l11_b.enabled = false
			MaxSceneCleaning_ro.l12_a.enabled = MaxSceneCleaning_ro.l12_b.enabled = false
		)

		format "---- Begin Scene Cleanup ----\n"
		local num_anim_layers = AnimLayerManager.getLayerCount()
		if num_anim_layers != 0 do
			format "% Anim Layers in Anim Layer Control Manager\n" num_anim_layers 
		MaxSceneCleaning_ro.l8_b.text = num_anim_layers as string
		local num_anim_layers_deleted = 0
		
		local MaxMotionClipMaster_instance = undefined
		local MaxMotionClipMaster_subAnim = trackViewNodes[#Max_MotionClip_Manager]
		if MaxMotionClipMaster_subAnim != undefined do
			MaxMotionClipMaster_instance = MaxMotionClipMaster_subAnim.object
		if MaxMotionClipMaster_instance != undefined then
		(
			format "A MaxMotionClipMaster instance was found.\n"
			local num_noteTracks = numNoteTracks MaxMotionClipMaster_instance
			format "% NoteTracks in MaxMotionClipMaster\n" num_noteTracks 
			local num_notetracks_deleted = 0
			
			local clipAssociations = MaxMotionClipMaster_instance.clipassociations
			local num_clipAssociations =clipAssociations.count
			format "% Clip Associations in MaxMotionClipMaster\n" num_clipAssociations 
			local num_clipAssociations_deleted = 0
			
			MaxSceneCleaning_ro.l1_b.text = num_noteTracks as string
			MaxSceneCleaning_ro.cb_key_check.checked = perform_notetrack_key_value_check_default
			MaxSceneCleaning_ro.l5_b.text = num_clipAssociations as string
			
			local track_index = 1
			
			with undo off 
			(
				for i = num_noteTracks to 1 by -1 while not MaxSceneCleaning_ro.cb_abort.checked do 
				(
					MaxSceneCleaning_ro.l2_b.text = (num_noteTracks-i+1) as string
					local note_track = getNoteTrack MaxMotionClipMaster_instance track_index
					local key_count = note_track.keys.count
					MaxSceneCleaning_ro.l3_b.text = key_count as string
					local all_bad_content = key_count != 0
					if MaxSceneCleaning_ro.cb_key_check.checked do
					(
						for j = 1 to key_count while all_bad_content do
						(
							local key_content = note_track.keys[j].value
							all_bad_content = (key_content == bad_notetrack_key_content) or (key_content == bad_notetrack_key_content2)
						)
					)
					if all_bad_content then
					(
						deleteNoteTrack MaxMotionClipMaster_instance note_track
						num_notetracks_deleted += 1
						MaxSceneCleaning_ro.l4_b.text = num_notetracks_deleted as string
					)
					else
						track_index += 1
					windows.processpostedmessages()
				)
			)
			MaxSceneCleaning_ro.cb_key_check.checked = false
			MaxSceneCleaning_ro.cb_key_check.enabled = false
			
			-- we will move the used clip associations to the beginning of the clipassociations param array and then
			-- set the param array's count to the number of used clip associations
			if not MaxSceneCleaning_ro.cb_abort.checked do with undo off 
			(
				local good_clip_index = 0 
				for i = 1 to num_clipAssociations do  -- look at each element
				(
					MaxSceneCleaning_ro.l6_b.text = i as string
					local unused = false
					local ca = clipAssociations[i]
					if ca.bipNode == undefined then
					(
						local theNodes = ca.nodes
						local hasNodes = false
						for theNode in theNodes while not hasNodes do
							hasNodes = theNode != undefined
						if not hasNodes do
							unused = true
					)
					if not unused then
					(
						good_clip_index += 1
						if i != good_clip_index do 
							clipAssociations[good_clip_index] = ca
					)
					else
					(
						num_clipAssociations_deleted += 1
						MaxSceneCleaning_ro.l7_b.text = num_clipAssociations_deleted as string
					)
				)
				if clipAssociations.count != good_clip_index do 
				(
					clipAssociations.count = good_clip_index
				)
				clipAssociations = undefined
			)

			if num_notetracks_deleted != 0 do format "Deleted % NoteTracks from MaxMotionClipMaster\n" num_notetracks_deleted 
			if num_clipAssociations_deleted != 0 do format "Deleted % Clip Associations from MaxMotionClipMaster\n" num_clipAssociations_deleted 
		)
		else
		(
			MaxSceneCleaning_ro.cb_key_check.checked = false
			MaxSceneCleaning_ro.cb_key_check.enabled = false
			-- format "No MaxMotionClipMaster instance present.\n"
		)

		with undo off
		(
			local AnimLayers = trackViewNodes[#Anim_Layer_Control_Manager].object.AnimLayers
			local n_deleted = 0
			for i = num_anim_layers to 2 by -1 while not MaxSceneCleaning_ro.cb_abort.checked do
			(
				-- the anim layer can be deleted if it contains no layer controllers
				local okToDelete = true
				local animLayer = AnimLayers[i]
				local nrefs = refs.getnumrefs animLayer
				for j = 2 to nrefs while okToDelete do  -- ref 1 is pb
				(
					local ref = refs.getreference animLayer j
					okToDelete =  ref == undefined or (classof ref == NodeMonitor)
				)
				if (MaybeDeleteAnimLayer AnimLayers i) do
				(
					n_deleted += 1
					MaxSceneCleaning_ro.l9_b.text = n_deleted as string
					windows.processpostedmessages()
				)
			)
			if n_deleted != 0 do 
				format "Deleted % Anim Layers from Anim Layer Control Manager\n" n_deleted
		)
		
		if perform_trackview_node_notetrack_check do
		(
			if not MaxSceneCleaning_ro.cb_abort.checked do with undo off
			(
				MaxSceneCleaning_ro.l11_b.text = "searching"
				local found = #()
				local nFound = countTVNoteTracks found:found
				if nFound != 0 do
					format "% NoteTracks found in Trackview Nodes\n" nFound
				if not MaxSceneCleaning_ro.cb_abort.checked then
				(
					MaxSceneCleaning_ro.l11_b.text = nFound as string
					if nFound != 0 do
					(
						local msg = "Found following NoteTracks on following Trackview nodes. Delete?\n"
						for p in found do msg += p.v1 + " - " + (p.v2 as string)
						-- res = queryBox msg title:"TrackView NoteTracks found"
						-- if res do 
						(
							local nDeleted = cleanTVNoteTracks()
							format "Deleted % NoteTracks from Trackview Nodes\n" nDeleted
						)
					)
				)
				else
					MaxSceneCleaning_ro.l11_b.text = "search aborted"
			)
		)
		
		MaxSceneCleaning_ro.cb_abort.enabled = false
		if MaxSceneCleaning_ro.cb_abort.checked do 
			format "Processing aborted\n"

		-- format "---- End Scene Cleanup ----\n"
		if close_dialog_when_done do
			destroydialog MaxSceneCleaning_ro
		ok
	),
	
	on create do
	(
		callbacks.removeScripts id:#cleanScene
		::cleanScene_instance = this
		callbacks.addScript #filePostOpen "::cleanScene_instance.cleanScene()" id:#cleanScene 
		callbacks.addScript #filePostMerge "::cleanScene_instance.cleanScene()" id:#cleanScene 
		cleanScene()
	)
)

cleanScene_def()

