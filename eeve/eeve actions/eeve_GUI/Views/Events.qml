import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //width: 1280
    //height: 720
    //anchors.fill: parent

    title: "Eventos"
    ListView {
        id: listViewActions
        x: 433
        width: 500
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50
        anchors.top: parent.top
        anchors.topMargin: 50
        anchors.horizontalCenter: parent.horizontalCenter
        objectName:"listview"
        delegate: Item {
            id: element
            x: 5
            width: listViewActions.width
            height: 55
            clip: true
            Row {
                id: row1
                anchors.verticalCenter: parent.verticalCenter
                spacing: 10
                //width: listView.width
                Rectangle {
                    width: listViewActions.width
                    height: 40
                    id: rectangle
                    color: colorCode
                    MouseArea{
                        anchors.fill:parent
                        z: 1
                        hoverEnabled: false

                        onClicked:{
                            eventsController.clickedEvent(rectangle, index, tag)
                        }
                    }

                    Text {
                        //id: name
                        text: name
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.bold: true
                    }

                    Row {
                        id: row
                        anchors.right: rectangle.right
                        anchors.verticalCenter: parent.verticalCenter
                        z:2
                        Switch {
                            id: switchEnable
                            checked:isEventEnabled

                            onClicked: {
                                eventsController.eventStateChanged(tag, switchEnable.checked)
                            }
                        }

                        PressAndHoldButton {
                            //text: "X"
                            source: "list-delete.png"
                            anchors.verticalCenter: parent.verticalCenter
                            onClicked:{
                                eventsController.deleteEvent(tag)
                            }
                        }
                    }


                }
            }
        }
        model: ListModel {
            
            id: sampleModel
            objectName:"listmodel"
            function addItem(newElement) {
                sampleModel.append(newElement)
            }
            function clearItems(a){
                sampleModel.clear()
            }
        }
    }

    RoundButton {
        id: importButton
        width: 75
        height: 75
        text: "i"
        /* source: "open-file.png" */
        anchors.right: parent.right
        anchors.rightMargin: 73
        anchors.bottom: addEventButton.top
        anchors.bottomMargin: 28

        onClicked: {
            eventsController.importFile()
        }
    }

    RoundButton {
        id: addEventButton
        width: 75
        height: 75
        text: "+"
        anchors.right: parent.right
        anchors.rightMargin: 73
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 58

        onClicked: {
            eventsController.addEvent()
        }
    }
}
