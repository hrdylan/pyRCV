import React from 'react';
import {useState} from 'react';
import {Input, Button} from '@material-ui/core'
import useFetch from './useFetch'
import { resolve } from 'url';

const styles = {
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

const pingServer = files => {
  if (!files) {
    return;
  }
  const reader = new FileReader()
  reader.onload = () => {
    fetch('http://localhost:4000').then(res => res.text()).then(data => {console.log(data)})
    fetch('http://localhost:4000/pyRCV', { method: 'POST', body: reader.result}).then(res => res.text()).then(data => {console.log(data)});
  }
  reader.onerror = () => {
    console.log('parse error');
  }

  reader.readAsText(files.item(0));
}
function FileSelector() {
  const [files, setFiles] = useState(0);
  const reader = new FileReader()
  return (
    <div style={styles.fileSelector}>
        <Input type={'file'} onChange={(event)=>{setFiles(event.target.files)}}></Input>
        <Button onClick={() => {pingServer(files)}}style={styles.button} variant={'outlined'} >Upload</Button>
    </div>
  );
}

export default FileSelector;
