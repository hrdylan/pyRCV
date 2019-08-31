import React from 'react';
import {Typography, Input, Button} from '@material-ui/core'
import FileSelector from './FileSelector'
import logo from './logo.svg';
import './App.css';

const styles = {
  app: {
    width: '100vw',
    height: '100vh',
    backgroundColor: 'white',
    display: 'flex',
    justifyContent: 'center',
    flexDirection: 'column'

  },
  header: {
    color: 'black',
    width: '100vw',
    height: '30vh',
    display: 'flex',
    alignItems: 'center',
    flexDirection: 'column'
  },
  fileSelector: {
    width: '100vw',
    height: '10vh',
    display: 'flex',
    alignItems: 'center',
    flexDirection: 'column'
  },
  button: {
    margin: '10px'
  }

}
function App() {
  return (
    <div style={styles.app}>
      <div style={styles.header}>
        <Typography variant={'h1'}>pyRCV</Typography>
        <br></br>
        <Typography variant={'subtitle1'}>a Rank Choice Voting (RCV) machine implemented in python</Typography>
      </div>
      <FileSelector/>
    </div>
  );
}

export default App;
