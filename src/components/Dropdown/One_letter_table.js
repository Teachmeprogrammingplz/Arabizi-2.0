import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


const font_size={
  fontSize:25,
}
const font_size_a={
  fontSize:25,
}
function One_letter_table(props) {
  return (
    <TableRow key={3*(props.index)+props.number}>
    <TableCell style={font_size}>
      {props.letter}
    </TableCell>
    <TableCell style={font_size}>{props.number}</TableCell>
    <TableCell style={font_size_a}>
      {props.bow}
    </TableCell>
  </TableRow>
  );
}
export default One_letter_table;