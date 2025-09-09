#
# Material Copier - PRO
#
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QMessageBox, QDockWidget
)
from PySide6.QtCore import Qt
from pymxs import runtime as rt

class SlateViewCopierPro(QWidget):
    def __init__(self, parent=None):
        super(SlateViewCopierPro, self).__init__(parent)
        
        self.setWindowTitle("Material Copier - PRO")
        self.resize(350, 240)
        
        self.main_layout = QVBoxLayout(self)
        
        # --- UI Elements ---
        self.source_label = QLabel("Source View:")
        self.source_combobox = QComboBox()
        self.dest_label = QLabel("Destination View:")
        self.dest_combobox = QComboBox()
        
        self.action_buttons_layout = QHBoxLayout()
        self.copy_button = QPushButton("Copy (Clone)")
        self.instance_button = QPushButton("Instance")
        self.action_buttons_layout.addWidget(self.copy_button)
        self.action_buttons_layout.addWidget(self.instance_button)

        # --- FIX: The layout for the bottom buttons was missing ---
        self.bottom_buttons_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh Lists")
        self.about_button = QPushButton("About")
        self.bottom_buttons_layout.addWidget(self.refresh_button)
        self.bottom_buttons_layout.addWidget(self.about_button)

        # Add widgets to layout
        self.main_layout.addWidget(self.source_label)
        self.main_layout.addWidget(self.source_combobox)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.dest_label)
        self.main_layout.addWidget(self.dest_combobox)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.action_buttons_layout)
        self.main_layout.addLayout(self.bottom_buttons_layout) # FIX: Add the bottom layout to the main layout
        
        # Connect signals
        self.refresh_button.clicked.connect(self.populate_view_comboboxes)
        self.about_button.clicked.connect(self.show_about_dialog) # FIX: Connect the about button
        self.copy_button.clicked.connect(lambda: self.perform_copy(method='copy'))
        self.instance_button.clicked.connect(lambda: self.perform_copy(method='instance'))
        
        self.populate_view_comboboxes()

    def show_about_dialog(self):
        about_text = """
        <b>Material Copier - PRO</b><br>
        Developed by Iman Shirani.<br>
        Version: 0.0.1 <br><br>
        <a href="https://github.com/imanshirani/Material-Copier-PRO">GitHub Project</a><br><br>        
        <a href='https://www.paypal.com/donate/?hosted_button_id=LAMNRY6DDWDC4'>Donate via PayPal</a>
        
        """
        QMessageBox.about(self, "Material Copier - PRO", about_text)

    def populate_view_comboboxes(self):
        self.source_combobox.clear()
        self.dest_combobox.clear()
        
        sme = rt.sme
        if not sme.isOpen: return
        num_views = sme.GetNumViews()
        view_names = [sme.getView(i).name for i in range(1, num_views + 1)]
        self.source_combobox.addItems(view_names)
        self.dest_combobox.addItems(view_names)
        if len(view_names) > 1: self.dest_combobox.setCurrentIndex(1)

    def perform_copy(self, method='copy'):
        source_view_index = self.source_combobox.currentIndex() + 1
        dest_view_index = self.dest_combobox.currentIndex() + 1
        
        if source_view_index == dest_view_index:
            QMessageBox.warning(self, "Warning", "Source and destination views cannot be the same.")
            return

        try:
            sme = rt.sme
            if not sme.isOpen: return

            source_view = sme.getView(source_view_index)
            dest_view = sme.getView(dest_view_index)
            
            selected_nodes = source_view.GetSelectedNodes()
            
            if not selected_nodes:
                QMessageBox.information(self, "Info", "No nodes selected.")
                return
            
            for node in selected_nodes:
                original_material = node.reference
                if original_material is None:
                    continue
                
                if method == 'copy':
                    new_material = rt.copy(original_material)
                else:
                    new_material = original_material
                
                original_position = node.position
                dest_view.createNode(new_material, original_position)

            QMessageBox.information(self, "Success", 
                                    f"{len(selected_nodes)} node(s) were processed as '{method}'.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred.\n\nDetails: {e}")


# --- YOUR DOCKING CODE - UNCHANGED ---
def main():   
    global main_dock_widget    
    
    try:
        if main_dock_widget:
            main_dock_widget.close()
    except Exception:
        pass

    
    max_hwnd = rt.windows.getMAXHWND()
    max_qwidget = QWidget.find(max_hwnd)    
    slate_copier_ui = SlateViewCopierPro(parent=max_qwidget) 
   
    main_dock_widget = QDockWidget("Material Copier - PRO", parent=max_qwidget)
    main_dock_widget.setObjectName("SlateViewCopierProDock_Unique")   
    main_dock_widget.setWidget(slate_copier_ui)       
    main_dock_widget.setFloating(True)
    main_dock_widget.show()

if __name__ == "__main__":
    main()