import QtQuick 2.12
import QtQuick.Controls 2.5

Page {
    id: page
    //anchors.fill: parent

    title: "Editar Gatilho"
    Rectangle {
        color: "transparent"
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 35
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
        width: 500

        Rectangle {
            width: parent.width
            height: 55
            color: "#DDA0DD"
            anchors.margins: 2
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            id:triggerName

            ComboBox {
                objectName: "triggersComboBox"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                width: 300
                model: ListModel{
                    id:tlm
                    objectName:"tlm"
                    function addItem(newElement) {
                        tlm.append({text : newElement})
                    }
                    function clearItems(a){
                        tlm.clear()
                    }
                }
                onCurrentIndexChanged:{
                    editTriggerController.triggerChanged(tlm.get(currentIndex).text)
                }
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
            id: argList
            objectName:"argList"
            anchors.top: triggerName.bottom
            anchors.bottom: addArgButton.top
            anchors.horizontalCenter: parent.horizontalCenter


            delegate: Rectangle {
                id:element
                objectName:"somerectangle"
                width: parent.width
                clip: true
                height: 40
                color: "transparent"

                TextField {
                    id:argValue
                    objectName:"argValue"
                    width: 230
                    height: parent.height
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    text: value
                    selectByMouse: true
                    onEditingFinished:{
                        editTriggerController.argsChanged(tag, argValue.text)
                    }
                }

                PressAndHoldButton {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    source: "list-delete.png"
                    onClicked:{
                        editTriggerController.deleteArg(tag)
                    }
                }
            }
            model: ListModel {
                id:argListModel
                objectName:"listmodelargs"
                function addItem(newElement) {
                    argListModel.append(newElement)
                }
                function clearItems(a){
                    argListModel.clear()
                }
                function gi(a){
                    var values = [];
                    for(var i = 0; i < argListModel.count; ++i){
                        values.push(argListModel.get(i).name)
                    }
                    console.log(values)
                    editTriggerController.argsChanged(argListModel, values);
                }
            }
        }
        RoundButton {
            width: 75
            height: 75
            text: "+"
            id: addArgButton
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                //argListModel.append({name:"argument"})
                editTriggerController.addTriggerArgument()
            }
        }
    }
}
