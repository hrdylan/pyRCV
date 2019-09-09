import React from 'react';
import { HorizontalBar } from 'react-chartjs-2'
import {useState} from 'react';
import generate from 'string-to-color';
import {Input, Button, TextField} from '@material-ui/core'
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

const pingServer = (files, setResults) => {
  if (!files) {
    return;
  }
  const reader = new FileReader()
  reader.onload = () => {

    fetch('http://localhost:4000/pyRCV', { method: 'POST', body: reader.result}).then(res => res.json()).then(data => {
      console.log(data)
      const rounds = Object.values(data);
      const datasets = rounds.map((val, index) => {
        console.log(val)
        return {
          datasets: [{
            data: Object.values(val.counts),
            backgroundColor: Object.keys(val.counts).map((label) => generate(label) )
          }],
    
          // These labels appear in the legend and in the tooltips when hovering different arcs
          labels: Object.keys(val.counts),
          title: `Round ${index}`
        }
      }
  
      );
      setResults(datasets);

    });
    
  }
  reader.onerror = () => {
    console.log('parse error');
  }

  reader.readAsText(files.item(0));
}
function FileSelector() {
  const [files, setFiles] = useState(0);
  const [results, setResults] = useState([]);
  const charts = results.map((dataset) => {
    console.log(dataset)
    return (
      <HorizontalBar data={dataset} options={{
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        title: dataset.title
      }}/>
    )
  });
  const reader = new FileReader()
  return (
    <div style={styles.fileSelector}>
        <Input type={'file'} onChange={(event)=>{setFiles(event.target.files)}}></Input>
        <Button onClick={() => {pingServer(files, setResults)}}style={styles.button} variant={'outlined'} >Upload</Button>
        <TextField fullWidth={true} value={results} variant="outlined" multiline={true}/>
        {charts}
    </div>
  );
}

export default FileSelector;
