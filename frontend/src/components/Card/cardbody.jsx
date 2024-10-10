import { Card, Dropdown, ListGroup, Button } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import { useState, useEffect } from "react";
import { LinkContainer } from 'react-router-bootstrap'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import SpinnerButton from '../SpinnerButton'

function CardBody({ selectedItem, data, onSelectItem, items, requestData }) {
    const [isClicked, setIsClicked] = useState(false);
    const handleSelect = (eventKey) => {
        onSelectItem(eventKey.target.id);
      };
    async function sendPriceTask() {
        const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\task_queue\\${selectedItem}`,
         {method: 'GET',});
        const requestData = await response.json()
        return requestData.task_id
    }

  return (
<div>
   <Row>
        <Col>
            <Card.Img src={data.image_url} variant="top" />
        </Col>
        <Col>
            <Card.Body className="p-4">
            <Card.Title>{requestData.name}</Card.Title>
            <Card.Text>
                {data.foiling.name}
            </Card.Text>
            </Card.Body>
            <Row>
                <Col>
                    <Dropdown className="mb-4">
                       <Dropdown.Toggle variant="success" id="dropdown-basic">
                         Choose version
                       </Dropdown.Toggle>
                       <Dropdown.Menu>
                            {Object.entries(items).map(item => <Dropdown.Item key={item[0]} id={item[0]} onClick={handleSelect}>{item[1]}</Dropdown.Item>)}
                       </Dropdown.Menu>
                     </Dropdown>
                </Col>
                <Col>
                    <LinkContainer to={`../cardData/${selectedItem}`}>
                        <Button variant="outline-info">Info</Button>
                    </LinkContainer>
                </Col>
                <Col>
                    <SpinnerButton clicked={isClicked} onClick={setIsClicked} callbackFunc={sendPriceTask}/>
                </Col>
            </Row>
        </Col>
    </Row>
</div>
  );
}
export default CardBody;