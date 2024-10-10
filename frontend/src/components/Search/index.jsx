import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

function BasicExample({setData}) {
    const { pageNumb } = useParams();
    console.log(pageNumb)
    function onClick(e) {
        e.preventDefault()
        console.log(e)
    }
  return (
    <Form>
    <Container>
        <Row>
        <Col>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <FloatingLabel controlId="floatingSelect" label="Works with selects">
              <Form.Select aria-label="Floating label select example">
                {setData.map(item => <option key={item.name}>{item.name}</option>)}
              </Form.Select>
            </FloatingLabel>
          </Form.Group>
          </Col>
          <Col>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <FloatingLabel controlId="floatingSelect" label="Works with selects">
              <Form.Select aria-label="Floating label select example">
                <option>Open this select menu</option>
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </Form.Select>
            </FloatingLabel>
          </Form.Group>
          </Col>
          <Col>
          <Form.Group className="mb-3" controlId="formBasicPassword">
            <FloatingLabel controlId="floatingControl" label="Name">
            <Form.Control type="password" placeholder="Password" />
            </FloatingLabel>
          </Form.Group>
          </Col>
          <Col>
          <Button variant="primary" type="submit" onClick={onClick}>
            Submit
          </Button>
          </Col>
      </Row>
      </Container>
    </Form>
  );
}

export default BasicExample;