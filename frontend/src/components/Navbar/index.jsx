import useState from "react";
import Navbar from 'react-bootstrap/Navbar';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
function NavbarExample() {
  return (
<Navbar className="bg-body-tertiary justify-content-around">
      <Form>
        <InputGroup>
          <InputGroup.Text id="basic-username">Username</InputGroup.Text>
          <Form.Control
            className="mx-4"
            placeholder="Username"
            aria-label="Username"
            aria-describedby="basic-username"
          />
          <InputGroup.Text id="basic-password">Password</InputGroup.Text>
          <Form.Control
            className="mx-4"
            type='password'
            placeholder="Password"
            aria-label="Password"
            aria-describedby="basic-password"
          />
            <Button className="mx-4" type="submit">Submit</Button>
        </InputGroup>
      </Form>
    </Navbar>
  );
}

export default NavbarExample;