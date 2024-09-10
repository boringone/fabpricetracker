import { Card, Dropdown, ListGroup, Button } from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import { useState, useEffect } from "react";
import { LinkContainer } from 'react-router-bootstrap'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
function CardBody({ selectedItem, data, onSelectItem, items, requestData }) {
    const handleSelect = (eventKey) => {
        onSelectItem(eventKey.target.id);
      };
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
                     <Dropdown className="mb-4">
           <Dropdown.Toggle variant="success" id="dropdown-basic">
             Choose version
           </Dropdown.Toggle>
           <Dropdown.Menu>
                {Object.entries(items).map(item => <Dropdown.Item key={item[0]} id={item[0]} onClick={handleSelect}>{item[1]}</Dropdown.Item>)}
           </Dropdown.Menu>
         </Dropdown>
          <LinkContainer to={`../cardData/${selectedItem}`}>
            <Button variant="outline-info">Info</Button>
        </LinkContainer>
    </Col>
      </Row>


      </div>
  );
}
export default CardBody;