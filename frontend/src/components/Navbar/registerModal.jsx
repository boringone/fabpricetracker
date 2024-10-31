import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState, useEffect } from "react";
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function RegisterModal() {
    const [modalShow, setModalShow] = useState(false);
    async function useLoginEndpoint(e){
            e.preventDefault()
            const formData = new FormData(e.target)
            let data = {}
            formData.forEach((value, key) => data[key] = value);
            const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\auth\\jwt\\create\\`,
                {method: 'POST', body: JSON.stringify(data), headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }})
            console.log(await response.json())
        }
  return (
      <>
   <Button variant="primary" className="mx-3" onClick={() => setModalShow(true)}>
    Sign up
  </Button>
    <Modal
    show={modalShow}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header>
        <Modal.Title id="contained-modal-title-vcenter">
          Sign up form
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={useLoginEndpoint}>
          <Form.Group className="mb-3" controlId="email_input">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" name='email' placeholder="name@example.com" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="password_input">
            <Form.Label>Password</Form.Label>
            <Form.Control name='password' type="password" />
          </Form.Group>
          <Form.Group className="mb-3" controlId="confirm_password_input">
            <Form.Label>Confirm password</Form.Label>
            <Form.Control name='password_confirm' type="password" />
          </Form.Group>
          <Row className="text-center">
              <Button variant="success" type="submit">Success</Button>
          </Row>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={() => setModalShow(false)}>Close</Button>
      </Modal.Footer>
    </Modal>
    </>
  );
}
export default RegisterModal;