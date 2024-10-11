import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";

function BasicExample({setData, typeData, onSubmit}) {
    let [searchParams, setSearchParams] = useSearchParams();
    function handleSearchChange(e) {
        e.preventDefault()
        const setSelect = document.getElementById('setSelect')
        const typeSelect = document.getElementById('typeSelect')
        const nameInput = document.getElementById('nameInput')
        onSubmit({set: setSelect.value, type: typeSelect.value, name: nameInput.value, pageNumb: 1})
    }
  return (
    <Form>
    <Container>
        <Row>
        <Col>
          <Form.Group className="mb-3">
            <FloatingLabel controlId="setSelect" label="Choose set">
              <Form.Select defaultValue={searchParams.get('set')}>
                {setData.map(item => <option key={item.name}>{item.name}</option>)}
              </Form.Select>
            </FloatingLabel>
          </Form.Group>
          </Col>
          <Col>
          <Form.Group className="mb-3">
            <FloatingLabel controlId="typeSelect" label="Choose card type">
              <Form.Select defaultValue={searchParams.get('type')}>
                {typeData.map(item => <option key={item}>{item}</option>)}
              </Form.Select>
            </FloatingLabel>
          </Form.Group>
          </Col>
          <Col>
          <Form.Group className="mb-3" controlId="formBasicPassword">
            <FloatingLabel controlId="nameInput" label="Card Name">
            <Form.Control type="text"/>
            </FloatingLabel>
          </Form.Group>
          </Col>
          <Col>
          <Button variant="primary" type="submit" onClick={handleSearchChange}>
            Submit
          </Button>
          </Col>
      </Row>
      </Container>
    </Form>
  );
}

export default BasicExample;