import QtQuick 2.12
import QtQuick.Controls 2.5

ApplicationWindow {
    id: window
    visible: true
    width: 1080
    height:700
    minimumWidth: 850
    minimumHeight: 500

    title: qsTr("EEVE")
    
    header: ToolBar {
        contentHeight: toolButton.implicitHeight
        background: Rectangle {
            color: "#8B008B"
        }

        ToolButton {
            id: toolButton
            text: stackView.depth > 1 ? "\u25C0" : "\u2630"
            font.pixelSize: Qt.application.font.pixelSize * 1.6
            onClicked: {
                if (stackView.depth > 1) {
                    controller.popView()
                    stackView.pop()
                } else {
                    //drawer.open()
                }
            }
        }

        Label {
            text: stackView.currentItem.title
            anchors.centerIn: parent
            font.pointSize: 13
        }
    }
    Drawer {
        id: drawer
        width: window.width * 0.66
        height: window.height

        Column {
            anchors.fill: parent

            ItemDelegate {
                text: qsTr("Login")
                width: parent.width
                onClicked: {
                    stackView.push("Login.qml")
                    drawer.close()
                }
            }
            ItemDelegate {
                text: qsTr("Events")
                width: parent.width
                onClicked: {
                    stackView.push("Events.qml")
                    drawer.close()
                }
            }
            ItemDelegate {
                text: qsTr("Edit Event")
                width: parent.width
                onClicked: {
                    stackView.push("EditEvent.qml")
                    drawer.close()
                }
            }
            ItemDelegate {
                text: qsTr("Edit Trigger")
                width: parent.width
                onClicked: {
                    stackView.push("EditTrigger.qml")
                    drawer.close()
                }
            }
            ItemDelegate {
                text: qsTr("Edit Action")
                width: parent.width
                onClicked: {
                    stackView.push("EditAction.qml")
                    drawer.close()
                }
            }
        }
    }
    StackView {

        id: stackView
        initialItem: "Login.qml"
        anchors.fill: parent

    Connections {
        target:controller

        onViewPushed:{
            stackView.push(viewName)
        }

        onEventAdded:{
            sampleModel.append({name: "~TEst", colorCode: "#DDA8DD"})
        }
    }
    }
}
