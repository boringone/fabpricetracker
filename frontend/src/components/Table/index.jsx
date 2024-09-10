import Table from 'react-bootstrap/Table';

function TableComponent({ requestData }) {
  return (
    <Table striped bordered hover size="sm">
      <thead>
        <tr>
          <th>#</th>
          <th>Seller name</th>
          <th>Card condition</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
      {requestData.map((item, currIndex) => {
      return <tr key={item.id}>
          <td>{currIndex}</td>
          <td>{item.seller_name}</td>
          <td>{item.card_condition}</td>
          <td>{item.card_price}</td>
        </tr>})}
      </tbody>
    </Table>
  );
}

export default TableComponent;