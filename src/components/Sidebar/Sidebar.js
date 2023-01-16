import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';


import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink,
} from 'react-router-dom';
import './Sidebar.css';
import Dropdown from '../Dropdown/Dropdown'
import Guess from '../Guess/Guess' 
import Predict from '../Predict_root/Predict_root.js' 
import Footer from "../Footer/footer.js"
import { FcFaq } from 'react-icons/fc';
import { FcIdea } from 'react-icons/fc';
import { FcReadingEbook } from 'react-icons/fc';
import {FaArrowAltCircleLeft} from "react-icons/fa";
const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function PersistentDrawerLeft() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <><Box className="flex">
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar className="header_style">
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          {/* <Typography variant="h6" noWrap component="div"> */}
          <div style={{ textAlign: "center" }}>
            <span style={{ fontWeight: "bold", color: "#FF6600", fontSize: "1.4em", marginRight: "2.5%" }}>
              MOAL
            </span>
            <font style={{ fontSize: 22, fontWeight: "bold", color: "#FFFFFF" }}>
              :
              <span style={{ color: "#FF6600", fontWeight: "bold", fontSize: "1.4em", marginLeft: "2.5%" }}>
                M
              </span>
              <span style={{ fontSize: "0.8em", color: "#FFFFFF" }}>EANING</span>
              <span style={{ color: "#FF6600", fontWeight: "bold", fontSize: "1.4em", marginLeft: "2.5%" }}>
                O
              </span>
              <span style={{ fontSize: "0.8em", color: "#FFFFFF" }}>F</span>
              <span style={{ color: "#FF6600", fontWeight: "bold", fontSize: "1.4em", marginLeft: "2.5%" }}>
                A
              </span>
              <span style={{ fontSize: "0.8em", color: "#FFFFFF" }}>RABIC</span>
              <span style={{ color: "#FF6600", fontWeight: "bold", fontSize: "1.4em", marginLeft: "2.5%" }}>
                L
              </span>
              <span style={{ fontSize: "0.8em", color: "#FFFFFF" }}>ETTERS</span>
            </font>
          </div>
          {/* </Typography> */}
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader style={{ height: '9.5%' }}>
          <Button onClick={handleDrawerClose} style={{ height: '100%', width: '100%' }}>
            {theme.direction === 'ltr' ?  <FaArrowAltCircleLeft className="Icon Hover_noglow" />: <ChevronRightIcon />}
          </Button>
        </DrawerHeader>
        <Divider />
        <List>
          <NavLink to='/dropdown' activeClassName="active" style={{ textDecoration: 'inherit' }}>
            <ListItem key={"Bag Of Words"} disablePadding className="Hover">
              <ListItemButton>
                <ListItemIcon >
                  <NavLink to='/dropdown'><FcFaq className="Icon" /></NavLink>
                </ListItemIcon>
                <ListItemText style={{color:'#ffa86e'}} primary={"Bag Of Words"} />

              </ListItemButton>
            </ListItem>
          </NavLink>

          <NavLink to='/guess' activeClassName="active" style={{ textDecoration: 'inherit' }}>
            <ListItem key={"Guess"} disablePadding className="Hover">
              <ListItemButton>
                <ListItemIcon>
                  <NavLink to='/guess'><FcIdea className="Icon" /></NavLink>
                </ListItemIcon>
                <ListItemText style={{color:'#ffa86e'}} primary={"Predict Root"} />

              </ListItemButton>
            </ListItem>
          </NavLink>

          
          <NavLink to='/predict' activeClassName="active" style={{ textDecoration: 'inherit' }}>
            <ListItem key={"Predict Root"} disablePadding className="Hover">
              <ListItemButton>
                <ListItemIcon>
                  <NavLink to='/predict'><FcReadingEbook className="Icon" /></NavLink>
                </ListItemIcon>
                <ListItemText style={{color:'#ffa86e'}} primary={"Guess"} />

              </ListItemButton>
            </ListItem>
          </NavLink>
        </List>
        <Divider />

      </Drawer>
      <Main open={open} className="main">
        <DrawerHeader />
        <Routes>
          <Route path='/' element={<Dropdown />}></Route>
          <Route path='/dropdown' element={<Dropdown />}></Route>
          <Route path='/guess' element={<Guess />}></Route>
          <Route path='/predict' element={<Predict />}></Route>
        </Routes>

      </Main>

    </Box><Footer className="footer"/></>
  );
}
