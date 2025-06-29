
incorrectBitmapSlot = "<-- incorrect/different config -->"
incorrectUserFlag = "<-- incorrect/different userFlags -->"

# MaterialFlag_Z.h
BitmapList = [
    incorrectBitmapSlot,
    "MTL_BITMAP_DECAL0",					# 1 
	"MTL_BITMAP_BLENDMASK",					# 2 
	"MTL_BITMAP_NORMAL",					# 3 
	"MTL_BITMAP_DIRT",						# 4 
	"MTL_BITMAP_ADD_DECAL0",				# 5 
	"MTL_BITMAP_ADD_NORMAL",				# 6 
	"MTL_BITMAP_EMISSIVE",					# 7 
	"MTL_BITMAP_DETAILDIFFUSE",				# 8 
	"MTL_BITMAP_DETAILNORMAL",				# 9 
	"MTL_BITMAP_WETNESS_AO",				# 10
	"MTL_BITMAP_METAL_ROUGH_AO",			# 11
	"MTL_BITMAP_DETAIL_METAL_ROUGH_AO",		# 12
	"MTL_BITMAP_ADD_METAL_ROUGH_AO",		# 13
	"MTL_BITMAP_OCCLUSION",					# 14
	"MTL_BITMAP_CLEARCOATCOLORROUGHNESS",	# 15
	"MTL_BITMAP_CLEARCOATNORMAL",			# 16
	"MTL_BITMAP_ANISO_DIR_ROUGH",			# 17
	"MTL_BITMAP_WIPERMASK",					# 18
	"MTL_BITMAP_WINDSHIELDDETAILNORMAL",	# 19
	"MTL_BITMAP_SCRATCHESNORMAL",			# 20
	"MTL_BITMAP_ALPHABLENDMASK",			# 21
	"MTL_BITMAP_IRIDESCENTTHICKNESS",		# 22
	"MTL_BITMAP_WINDSHIELDINSECTS",			# 23
	"MTL_BITMAP_WINDSHIELDINSECTSMASK",		# 24
	"MTL_BITMAP_DIRTOVERLAY_METAL_ROUGH_AO",# 25
	"MTL_BITMAP_TIREDETAILS",				# 26
	"MTL_BITMAP_TIREMUDNORMAL",				# 27
	"MTL_BITMAP_DIRTOVERLAY"				# 28
]
""" str list of materials flags, with index 0 beeing incorrect value """ 


def findBitmapIndex(entry) :
	"""	Return the index of the string of bitmap materials list (or 0 for invalid text) from str """
	for i in range(len(BitmapList)) :
		if BitmapList[i] == entry :
			return i
	return 0

# TODO: clean texture slot compatibility
compatibleIndexes = [
	[1, 5, 7],		# MTL_BITMAP_DECAL0, MTL_BITMAP_ADD_DECAL0, MTL_BITMAP_EMISSIVE
	[3, 6],			# MTL_BITMAP_NORMAL, MTL_BITMAP_ADD_NORMAL
	[4, 8],			# MTL_BITMAP_DIRT, MTL_BITMAP_DETAILDIFFUSE
	[10, 12],		# MTL_BITMAP_WETNESS_AO, MTL_BITMAP_DETAIL_METAL_ROUGH_AO
	[11, 13, 25],	# MTL_BITMAP_METAL_ROUGH_AO, MTL_BITMAP_ADD_METAL_ROUGH_AO, MTL_BITMAP_DIRT_METAL_ROUGH_AO
	[14],			# MTL_BITMAP_OCCLUSION
	[15],			# MTL_BITMAP_CLEARCOATCOLORROUGHNESS
	[16],			# MTL_BITMAP_CLEARCOATNORMAL
	[17],			# MTL_BITMAP_ANISO_DIR_ROUGH
	[18],			# MTL_BITMAP_WIPERMASK
	[19],			# MTL_BITMAP_WINDSHIELDDETAILNORMAL
	[20],			# MTL_BITMAP_SCRATCHESNORMAL
	[21],			# MTL_BITMAP_ALPHABLENDMASK
	[22],			# MTL_BITMAP_IRIDESCENTTHICKNESS
	[23],			# MTL_BITMAP_WINDSHIELDINSECTS
	[24],			# MTL_BITMAP_WINDSHIELDINSECTSMASK
	[26],			# MTL_BITMAP_TIREDETAILS
	[27],			# MTL_BITMAP_TIREMUDNORMAL
	[28],			# MTL_BITMAP_DIRTOVERLAY
]
""" Array of compatible bitmap slot index (MaterialFlagsData_Z.h, gMaterialBitmapsFlags) """ 

def compatibleBitmapIndex(index1, index2) :
	""" Return True if both index are compatibles """
	if index1 == 0 or index2 == 0 :
		return False
	if index1 == index2 :
		return True
	for c in compatibleIndexes :
		if (index1 in c) and (index2 in c) :
			return True
	return False


###################################################################################################


class BitmapConfig :
	""" Simple struct -> materialBitmap : int (0 is incorrect value) , userFlags : str , forceNoAlpha : bool (or None for incorrect value) """
	def __init__(self, pMaterialBitmap = 0, pUserFlags = incorrectUserFlag, pForceNoAlpha = None) :
		if pMaterialBitmap > len(BitmapList) or pMaterialBitmap < 0 :
			pMaterialBitmap = 0
		self.materialBitmap = pMaterialBitmap
		self.userFlags = pUserFlags
		self.forceNoAlpha = pForceNoAlpha

	def __str__(self) :
		return "(" + BitmapList[self.materialBitmap] + ", \"" + self.userFlags + "\", " + str(self.forceNoAlpha) + ")"

	@property
	def __name__(self) -> str:
		return BitmapList[self.materialBitmap]

def copyBitmapConfig(toCopy ) :
	""" Return a copy of a BitmapConfig object """
	return BitmapConfig(toCopy.materialBitmap, toCopy.userFlags, toCopy.forceNoAlpha)

def compareBitmapConfig(first, second) :
	""" Return true if the configs are the same """
	return (first.materialBitmap == second.materialBitmap) and (first.userFlags == second.userFlags) and (first.forceNoAlpha == second.forceNoAlpha)
