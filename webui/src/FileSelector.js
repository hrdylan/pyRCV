import React from 'react';
import {useState} from 'react';
import {Input, Button} from '@material-ui/core'

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
function FileSelector() {
  const [files, setFiles] = useState(0);
  const reader = new FileReader()
  for (var i = 0; i < files.length; i++){
    console.log(files.item(i))
    reader.readAsText(files.item(i));
  }
  return (
    <div style={styles.fileSelector}>
        <Input type={'file'} onChange={(event)=>{setFiles(event.target.files)}}></Input>
        <Button style={styles.button} variant={'outlined'} >Upload</Button>
    </div>
  );
}

export default FileSelector;
