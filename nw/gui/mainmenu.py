# -*- coding: utf-8 -*-
"""novelWriter GUI Main Menu

 novelWriter – GUI Main Menu
=============================
 Class holding the main window

 File History:
 Created: 2019-04-27 [0.0.1] (Split from winmain)

"""

import logging
import nw

from PyQt5.QtWidgets import qApp, QMenuBar, QAction
from PyQt5.QtGui     import QIcon

from nw.enum         import nwItemType, nwItemClass, nwDocAction

logger = logging.getLogger(__name__)

class GuiMainMenu(QMenuBar):

    def __init__(self, theParent, theProject):
        QMenuBar.__init__(self, theParent)

        logger.debug("Initialising Main Menu ...")
        self.mainConf   = nw.CONFIG
        self.theParent  = theParent
        self.theProject = theProject

        self._buildProjectMenu()
        self._buildDocumentMenu()
        self._buildEditMenu()
        self._buildViewMenu()
        self._buildFormatMenu()
        self._buildToolsMenu()
        self._buildHelpMenu()

        # Function Pointers
        self._docAction    = self.theParent.docEditor.docAction
        self._moveTreeItem = self.theParent.treeView.moveTreeItem
        self._newTreeItem  = self.theParent.treeView.newTreeItem

        logger.debug("Main Menu initialisation complete")

        return

    def openRecentProject(self, menuItem, recentItem):
        logger.verbose("User requested opening recent project #%d" % recentItem)
        self.theParent.openProject(self.mainConf.recentList[recentItem])
        return True

    ##
    #  Menu Action
    ##

    def _menuExit(self):
        self.theParent.closeMain()
        qApp.quit()
        return True

    def _showAbout(self):
        self.docTabs.createTab(None,nw.DOCTYPE_ABOUT)
        return True

    ##
    #  Menu Builders
    ##

    def _buildProjectMenu(self):

        # Project
        self.projMenu = self.addMenu("&Project")

        # Project > New Project
        menuItem = QAction(QIcon.fromTheme("folder-new"), "New Project", self)
        menuItem.setStatusTip("Create New Project")
        menuItem.triggered.connect(self.theParent.newProject)
        self.projMenu.addAction(menuItem)

        # Project > Open Project
        menuItem = QAction(QIcon.fromTheme("folder-open"), "Open Project", self)
        menuItem.setStatusTip("Open Project")
        menuItem.setShortcut("Ctrl+Shift+O")
        menuItem.triggered.connect(lambda : self.theParent.openProject(None))
        self.projMenu.addAction(menuItem)

        # Project > Save Project
        menuItem = QAction(QIcon.fromTheme("document-save"), "Save Project", self)
        menuItem.setStatusTip("Save Project")
        menuItem.setShortcut("Ctrl+Shift+S")
        menuItem.triggered.connect(self.theParent.saveProject)
        self.projMenu.addAction(menuItem)

        # Project > Recent Projects
        recentMenu = self.projMenu.addMenu(QIcon.fromTheme("document-open-recent"),"Recent Projects")
        for n in range(len(self.mainConf.recentList)):
            recentProject = self.mainConf.recentList[n]
            if recentProject == "": continue
            menuItem = QAction(QIcon.fromTheme("folder-open"), "%d: %s" % (n,recentProject), self.projMenu)
            menuItem.triggered.connect(lambda menuItem, n=n : self.openRecentProject(menuItem, n))
            recentMenu.addAction(menuItem)

        # Project > Project Settings
        menuItem = QAction(QIcon.fromTheme("document-properties"), "Project Settings", self)
        menuItem.setStatusTip("Project Settings")
        menuItem.triggered.connect(self.theParent.editProjectDialog)
        self.projMenu.addAction(menuItem)

        # Project > Separator
        self.projMenu.addSeparator()

        # Project > New Root
        rootMenu = self.projMenu.addMenu(QIcon.fromTheme("folder-new"), "Create Root Folder")
        self.rootItems = {}
        self.rootItems[nwItemClass.NOVEL]      = QAction(QIcon.fromTheme("folder-new"), "Novel Root",     rootMenu)
        self.rootItems[nwItemClass.PLOT]       = QAction(QIcon.fromTheme("folder-new"), "Plot Root",      rootMenu)
        self.rootItems[nwItemClass.CHARACTER]  = QAction(QIcon.fromTheme("folder-new"), "Character Root", rootMenu)
        self.rootItems[nwItemClass.WORLD]      = QAction(QIcon.fromTheme("folder-new"), "Location Root",  rootMenu)
        self.rootItems[nwItemClass.TIMELINE]   = QAction(QIcon.fromTheme("folder-new"), "Timeline Root",  rootMenu)
        self.rootItems[nwItemClass.OBJECT]     = QAction(QIcon.fromTheme("folder-new"), "Object Root",    rootMenu)
        self.rootItems[nwItemClass.CUSTOM]     = QAction(QIcon.fromTheme("folder-new"), "Custom Root",    rootMenu)
        rootMenu.addActions(self.rootItems.values())

        # Project > New Folder
        menuItem = QAction(QIcon.fromTheme("folder-new"), "Create Folder", self)
        menuItem.setStatusTip("Create Folder")
        menuItem.setShortcut("Ctrl+Shift+N")
        menuItem.triggered.connect(lambda : self._newTreeItem(nwItemType.FOLDER, None))
        self.projMenu.addAction(menuItem)

        # Project > Rename Folder
        menuItem = QAction(QIcon.fromTheme("folder-new"), "Rename Folder", self)
        menuItem.setStatusTip("Rename Selected Folder")
        menuItem.setShortcut("Ctrl+Shift+E")
        self.projMenu.addAction(menuItem)

        # Project > Delete Folder
        menuItem = QAction(QIcon.fromTheme("edit-delete"), "Delete Folder", self)
        menuItem.setStatusTip("Delete Selected Folder")
        menuItem.setShortcut("Ctrl+Shift+Del")
        self.projMenu.addAction(menuItem)

        # Project > Separator
        self.projMenu.addSeparator()

        # Project > Exit
        menuItem = QAction(QIcon.fromTheme("application-exit"), "Exit", self)
        menuItem.setStatusTip("Exit %s" % nw.__package__)
        menuItem.setShortcut("Ctrl+Q")
        menuItem.triggered.connect(self._menuExit)
        self.projMenu.addAction(menuItem)

        return

    def _buildDocumentMenu(self):

        # Document
        self.docuMenu = self.addMenu("&Document")

        # Document > New
        menuItem = QAction(QIcon.fromTheme("document-new"), "&New Document", self)
        menuItem.setStatusTip("Create New Document")
        menuItem.setShortcut("Ctrl+N")
        menuItem.triggered.connect(lambda : self._newTreeItem(nwItemType.FILE, None))
        self.docuMenu.addAction(menuItem)

        # Document > Open
        menuItem = QAction(QIcon.fromTheme("document-open"), "&Open Document", self)
        menuItem.setStatusTip("Open Selected Document")
        menuItem.setShortcut("Ctrl+O")
        menuItem.triggered.connect(self.theParent.openSelectedItem)
        self.docuMenu.addAction(menuItem)

        # Document > Save
        menuItem = QAction(QIcon.fromTheme("document-save"), "&Save Document", self)
        menuItem.setStatusTip("Save Current Document")
        menuItem.setShortcut("Ctrl+S")
        menuItem.triggered.connect(self.theParent.saveDocument)
        self.docuMenu.addAction(menuItem)

        # Document > Separator
        self.docuMenu.addSeparator()

        # Document > Edit
        menuItem = QAction(QIcon.fromTheme("document-properties"), "&Edit Document", self)
        menuItem.setStatusTip("Change Document Settings")
        menuItem.setShortcut("Ctrl+E")
        menuItem.triggered.connect(self.theParent.editItem)
        self.docuMenu.addAction(menuItem)

        # Document > Delete
        menuItem = QAction(QIcon.fromTheme("edit-delete"), "&Delete Document", self)
        menuItem.setStatusTip("Delete Selected Document")
        menuItem.setShortcut("Ctrl+Del")
        self.docuMenu.addAction(menuItem)

        # Document > Separator
        self.docuMenu.addSeparator()

        # Document > Split
        menuItem = QAction(QIcon.fromTheme("list-add"), "Split Document", self)
        menuItem.setStatusTip("Split Selected Document")
        self.docuMenu.addAction(menuItem)

        # Document > Merge
        menuItem = QAction(QIcon.fromTheme("list-remove"), "Merge Document", self)
        menuItem.setStatusTip("Merge Selected Documents")
        self.docuMenu.addAction(menuItem)

        return

    def _buildViewMenu(self):

        # View
        self.viewMenu = self.addMenu("&View")

        # View > TreeView
        menuItem = QAction(QIcon.fromTheme("go-home"), "TreeView", self)
        menuItem.setStatusTip("Move to TreeView Panel")
        menuItem.setShortcut("Ctrl+1")
        menuItem.triggered.connect(lambda : self.theParent.setFocus(1))
        self.viewMenu.addAction(menuItem)

        # View > Document Pane 1
        menuItem = QAction(QIcon.fromTheme("go-first"), "Left Document Pane", self)
        menuItem.setStatusTip("Move to Left Document Pane")
        menuItem.setShortcut("Ctrl+2")
        menuItem.triggered.connect(lambda : self.theParent.setFocus(2))
        self.viewMenu.addAction(menuItem)

        # View > Document Pane 2
        menuItem = QAction(QIcon.fromTheme("go-last"), "Right Document Pane", self)
        menuItem.setStatusTip("Move to Right Document Pane")
        menuItem.setShortcut("Ctrl+3")
        menuItem.triggered.connect(lambda : self.theParent.setFocus(3))
        self.viewMenu.addAction(menuItem)

        return

    def _buildEditMenu(self):

        # Edit
        self.editMenu = self.addMenu("&Edit")

        # Edit > Undo
        menuItem = QAction(QIcon.fromTheme("edit-undo"), "Undo", self)
        menuItem.setStatusTip("Undo Last Change")
        menuItem.setShortcut("Ctrl+Z")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.UNDO))
        self.editMenu.addAction(menuItem)

        # Edit > Redo
        menuItem = QAction(QIcon.fromTheme("edit-redo"), "Redo", self)
        menuItem.setStatusTip("Redo Last Change")
        menuItem.setShortcut("Ctrl+Y")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.REDO))
        self.editMenu.addAction(menuItem)

        # Edit > Separator
        self.editMenu.addSeparator()

        # Edit > Cut
        menuItem = QAction(QIcon.fromTheme("edit-cut"), "Cut", self)
        menuItem.setStatusTip("Cut Selected Text")
        menuItem.setShortcut("Ctrl+X")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.CUT))
        self.editMenu.addAction(menuItem)

        # Edit > Copy
        menuItem = QAction(QIcon.fromTheme("edit-copy"), "Copy", self)
        menuItem.setStatusTip("Copy Selected Text")
        menuItem.setShortcut("Ctrl+C")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.COPY))
        self.editMenu.addAction(menuItem)

        # Edit > Paste
        menuItem = QAction(QIcon.fromTheme("edit-paste"), "Paste", self)
        menuItem.setStatusTip("Paste Text from Clipboard")
        menuItem.setShortcut("Ctrl+V")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.PASTE))
        self.editMenu.addAction(menuItem)

        # Edit > Separator
        self.editMenu.addSeparator()

        # Edit > Select All
        menuItem = QAction(QIcon.fromTheme("edit-select-all"), "Select All", self)
        menuItem.setStatusTip("Select All Text in Document")
        menuItem.setShortcut("Ctrl+A")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.SEL_ALL))
        self.editMenu.addAction(menuItem)

        # Edit > Select Paragraph
        menuItem = QAction(QIcon.fromTheme("edit-select-all"), "Select Paragraph", self)
        menuItem.setStatusTip("Select All Text in Paragraph")
        menuItem.setShortcut("Ctrl+Shift+A")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.SEL_PARA))
        self.editMenu.addAction(menuItem)

        return

    def _buildFormatMenu(self):

        # Format
        self.fmtMenu = self.addMenu("&Format")

        # Format > Bold Text
        menuItem = QAction(QIcon.fromTheme("format-text-bold"), "Bold Text", self)
        menuItem.setStatusTip("Make Selected Text Bold")
        menuItem.setShortcut("Ctrl+B")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.BOLD))
        self.fmtMenu.addAction(menuItem)

        # Format > Italic Text
        menuItem = QAction(QIcon.fromTheme("format-text-italic"), "Italic Text", self)
        menuItem.setStatusTip("Make Selected Text Italic")
        menuItem.setShortcut("Ctrl+I")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.ITALIC))
        self.fmtMenu.addAction(menuItem)

        # Format > Underline Text
        menuItem = QAction(QIcon.fromTheme("format-text-underline"), "Underline Text", self)
        menuItem.setStatusTip("Underline Selected Text")
        menuItem.setShortcut("Ctrl+U")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.U_LINE))
        self.fmtMenu.addAction(menuItem)

        # Edit > Separator
        self.fmtMenu.addSeparator()

        # Format > Double Quotes
        menuItem = QAction(QIcon.fromTheme("insert-text"), "Wrap Double Quotes", self)
        menuItem.setStatusTip("Wrap Selected Text in Double Quotes")
        menuItem.setShortcut("Ctrl+D")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.D_QUOTE))
        self.fmtMenu.addAction(menuItem)

        # Format > Single Quotes
        menuItem = QAction(QIcon.fromTheme("insert-text"), "Wrap Single Quotes", self)
        menuItem.setStatusTip("Wrap Selected Text in Single Quotes")
        menuItem.setShortcut("Ctrl+Shift+D")
        menuItem.triggered.connect(lambda: self._docAction(nwDocAction.S_QUOTE))
        self.fmtMenu.addAction(menuItem)

        return

    def _buildToolsMenu(self):

        # Tools
        self.toolsMenu = self.addMenu("&Tools")

        # Tools > Move Up
        self.toolsMoveUp = QAction(QIcon.fromTheme("go-up"), "Move Tree Item Up", self)
        self.toolsMoveUp.setStatusTip("Move Item Up")
        self.toolsMoveUp.setShortcut("Ctrl+Shift+Up")
        self.toolsMoveUp.triggered.connect(lambda : self._moveTreeItem(-1))
        self.toolsMenu.addAction(self.toolsMoveUp)

        # Tools > Move Down
        self.toolsMoveDown = QAction(QIcon.fromTheme("go-down"), "Move Tree Item Down", self)
        self.toolsMoveDown.setStatusTip("Move Item Down")
        self.toolsMoveDown.setShortcut("Ctrl+Shift+Down")
        self.toolsMoveDown.triggered.connect(lambda : self._moveTreeItem(1))
        self.toolsMenu.addAction(self.toolsMoveDown)

        # Tools > Separator
        self.toolsMenu.addSeparator()

        # Tools > Settings
        menuItem = QAction(QIcon.fromTheme("preferences-system"), "Preferences", self)
        menuItem.setStatusTip("Preferences")
        self.toolsMenu.addAction(menuItem)

        return

    def _buildHelpMenu(self):

        # Help
        self.helpMenu = self.addMenu("&Help")

        # Help > About
        menuItem = QAction(QIcon.fromTheme("help-about"), "About %s" % nw.__package__, self)
        menuItem.setStatusTip("About %s" % nw.__package__)
        menuItem.triggered.connect(self._showAbout)
        self.helpMenu.addAction(menuItem)

        # Help > About Qt5
        menuItem = QAction(QIcon.fromTheme("help-about"), "About Qt5", self)
        menuItem.setStatusTip("About Qt5")
        self.helpMenu.addAction(menuItem)

        return

# END Class GuiMainMenu
