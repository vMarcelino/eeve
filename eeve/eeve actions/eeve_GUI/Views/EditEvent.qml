import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //width: 1280
    //height: 720
    //anchors.fill: parent

    title: "Editar Evento"
    Row {
        id:topRow
        anchors.horizontalCenter: parent.horizontalCenter
        height: 50

        Label {
            text: "Nome:    "
            anchors.verticalCenter:parent.verticalCenter
        }

        TextField {
            id:eventNameTextField
            width: 230
            height:parent.height
            text: "event zero"
            selectByMouse: true
            onEditingFinished:{
                editEventController.nameChanged(eventNameTextField.text)
            }
        }
    }
    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: topRow.bottom
        anchors.bottom: parent.bottom
        spacing: 10

        Rectangle {
            width: 500
            height: parent.height
            color: "transparent"

            Rectangle {
                height: 35
                width: parent.width
                color: "#DDA0DD"
                id: triggerLabel
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter

                Text {
                    text: "Gatilhos"
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter:parent.verticalCenter
                    font.bold: true
                    font.pointSize: 13
                }

                /* PressAndHoldButton {
                    anchors.right: parent.right
                    source: "open-file.png"
                    anchors.verticalCenter: parent.verticalCenter
                    width: 35
                    height: 35
                } */
            }

            ListView {
                width: parent.width
                spacing: 2
                id: triggerList
                anchors.top: triggerLabel.bottom
                anchors.bottom: triggerButton.top
                anchors.horizontalCenter: parent.horizontalCenter


                delegate: Rectangle {
                    id:element
                    width: parent.width
                    clip: true
                    height: 40
                    color: colorCode

                    MouseArea{
                        anchors.fill:parent
                        z: 1
                        hoverEnabled: false

                        onClicked:{
                            editEventController.clickedTrigger(element, index, tag)
                        }
                    }

                    Text {
                        text: name
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.bold: true
                    }

                    PressAndHoldButton {
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        source: "list-delete.png"
                        z:2

                        onClicked:{
                            editEventController.deleteTrigger(tag)
                        }
                    
                    }
                }
                model: ListModel {
                    id:triggerListModel
                    objectName:"listmodeltriggers"
                    function addItem(newElement) {
                        triggerListModel.append(newElement)
                    }
                    function clearItems(a) {
                        triggerListModel.clear()
                    }
                }
            }
            RoundButton {
                width: 75
                height: 75
                text: "+"
                id: triggerButton
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: {
                    editEventController.addTrigger()
                }
            }
        }
        Rectangle {
            width: 500
            height: parent.height
            color: "transparent"

            Rectangle {
                color: "#DDA0DD"
                height: 35
                width: parent.width
                id: actionLabel
                anchors.top: triggerButton.bottom
                anchors.horizontalCenter: parent.horizontalCenter

                Text {
                    text: "Ações"
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter:parent.verticalCenter
                    font.bold: true
                    font.pointSize: 13
                }

                /* PressAndHoldButton {
                    anchors.right: parent.right
                    source: "open-file.png"
                    anchors.verticalCenter: parent.verticalCenter
                    width: 35
                    height: 35
                } */
            }

            ListView {
                spacing: 2
                width: parent.width
                id: actionList
                anchors.top: actionLabel.bottom
                anchors.bottom: actionButton.top
                anchors.horizontalCenter: parent.horizontalCenter

                delegate: Rectangle {
                    id:element
                    width: parent.width
                    clip: true
                    height: 40
                    color: colorCode

                    MouseArea{
                        anchors.fill:parent
                        z: 1
                        hoverEnabled: false

                        onClicked:{
                            editEventController.clickedAction(element, index, tag)
                        }
                    }

                    Text {
                        text: name
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.bold: true
                    }

                    PressAndHoldButton {
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        source: "list-delete.png"
                        z:2

                        onClicked:{
                            editEventController.deleteAction(tag)
                        }
                    }
                }
                model: ListModel {
                    id:actionListModel
                    objectName:"listmodelactions"
                    function addItem(newElement) {
                        actionListModel.append(newElement)
                    }
                    function clearItems(a) {
                        actionListModel.clear()
                    }
                }
            }
            RoundButton {
                width: 75
                height: 75
                text: "+"
                id: actionButton
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: {
                    editEventController.addAction()
                }
            }
        }
    }
    Connections{
        target:editEventController
        onEventEditInitialized: {
            eventNameTextField.text = eventName
        }
    }
}
