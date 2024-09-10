import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Dropdown from 'react-bootstrap/Dropdown';
import { useState, useEffect } from "react";
import CardBody from './cardbody'


function CardExample({ requestData, itemData }) {
    const [selectedPrinting, setSelectedPrinting] = useState(itemData[0].unique_id);
    let selectedPrintingData
    for (let elem of itemData){
        if (elem.unique_id == selectedPrinting){
            selectedPrintingData = elem
        }
    }
    const items = Object.assign({}, ...itemData.map(item => ({[item.unique_id]: `${requestData.name} - ${item.set.name} ${item.edition.name} ${item.foiling.name}`})))
  return (
    <Card>
      <CardBody selectedItem={selectedPrinting}
        data={selectedPrintingData}
        onSelectItem={setSelectedPrinting}
        items={items}
        requestData={requestData}/>
    </Card>
  );
}

export default CardExample;