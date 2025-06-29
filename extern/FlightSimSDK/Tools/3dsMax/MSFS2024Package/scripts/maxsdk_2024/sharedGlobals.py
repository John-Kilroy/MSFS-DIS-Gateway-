#To cancel export, we use a global var defined outside of the multi exporter to be able to retrieve it from multiple places... Yes this is ugly and should be done differently
G_ME_cancelExport = False

#Hold mesh inspector window reference
G_ME_meshInspectorWindow = None
