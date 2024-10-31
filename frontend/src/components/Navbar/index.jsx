import useState from "react";
import Navbar from 'react-bootstrap/Navbar';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import LoginModal from './loginModal'
import RegisterModal from './registerModal'
function NavbarExample(loggedIn) {
  return (
<Navbar className="bg-body-tertiary justify-content-end">
    <LoginModal/>
    <RegisterModal/>
    </Navbar>
  );
}

export default NavbarExample;