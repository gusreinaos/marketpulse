//Author: Aditya Kadkhikar, Burak Askan
import { useEffect, useState } from 'react'
import ModelService from '../../../services/modelService'
import Dropdown from 'react-bootstrap/Dropdown'
import { FileUploadBox } from '../UploadFileComponent/upload-file-component';
import styles from './models-list-component.module.scss'
import Button from 'react-bootstrap/Button';

interface ModelsListComponentProps {
    modelName: string;
}

export const ModelsListComponent: React.FC<ModelsListComponentProps> = ({modelName}) => {
    const [versions, setVersions] = useState<string[]>([]);
    const [currentModel, setCurrentModel] = useState<string>("")
    const [productionModel, setProductionModel] = useState<string>("")
    const [loading, setLoading] = useState(true);
    const [modelInfo, setModelInfo] = useState({
        model: currentModel,
        summary: '',
        history: {
            accuracy: '',
            loss: ''
        },
        heatmap: '' 
    })

    useEffect(()=> {
        if(modelName === 'Sentiment Model'){
            ModelService.getSentimentModels().then((val) => {
                setVersions(JSON.parse(val).model_vers);
            }).catch((err) => {
                console.log(err);
            });
            ModelService.getSentimentProductionModel().then((val) => {
                console.log(val)
                setProductionModel(val.response);
            }).catch((err) => {
                console.log(err);
            });
        } else if(modelName === 'Market Trend Model'){
            ModelService.getMarketTrendModels().then((val) => {
                setVersions(JSON.parse(val).model_vers);
            }).catch((err) => {
                console.log(err);
            });
            ModelService.getMarketTrendProductionModel().then((val) => {
                setProductionModel(val.response);
            }).catch((err) => {
                console.log(err);
            });
        }
    }, [])

    useEffect(()=> {
        if (currentModel != '') {
                setLoading(true);
                if(modelName === 'Sentiment Model'){
                    ModelService.getSentimentModel(currentModel).then((info) => {
                        setModelInfo(oldInfo => ({
                            ...oldInfo, 
                            ...info
                        }));
                        setLoading(false);
                    }).catch((err) => {
                        console.log(err);
                    });
                } else if(modelName == 'Market Trend Model'){
                    ModelService.getMarketTrendModel(currentModel).then((info) => {
                        setModelInfo(oldInfo => ({
                            ...oldInfo, 
                            ...info
                        }));
                        setLoading(false);
                    }).catch((err) => {
                        console.log(err);
                    });
                }
        }
    }, [currentModel])
    

    const updateVersions = (newValue: string) => {
        setVersions((prevArray) => [...prevArray, newValue]);
        setCurrentModel(newValue)
      };

    const setPredictionModel = () => {
        if(modelName == 'Sentiment Model') {
            ModelService.setPredictionSentimentModel(currentModel)
            setProductionModel(currentModel)
        }else if(modelName == 'Market Trend Model') {
            ModelService.setPredictionTrendModel(currentModel)
            setProductionModel(currentModel)
        }
        
    }


    const getModelSummary = () => {
        const layers = (JSON.parse(modelInfo.summary).config.layers)
        let arr = []
        for (let index = 0; index < layers.length; index++) {
            let units = (layers[index].config.input_dim != undefined || layers[index].config.output_dim != undefined) ? 
            `(${layers[index].config.input_dim}, ${layers[index].config.output_dim})` : 
            `(${layers[index].config.units})`
            
            if (layers[index].config.layer != undefined) {
                units = (layers[index].config.layer.config.units)
            }
            arr.push(
                JSON.stringify({
                'type': layers[index].class_name,
                'dtype': layers[index].config.dtype,
                'units': units,
                })
            );
        }
        return arr;
    }

    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
            <Dropdown>
                <Dropdown.Toggle size='sm' style={{margin: '30px', padding: '10px 30px', fontSize: '18px'}} variant="primary" id="dropdown-basic">
                    {currentModel != ''? currentModel : "Select a model"}
                </Dropdown.Toggle>

                <Dropdown.Menu style={{overflowY:'scroll', height:'100px'}}>
                        <Dropdown.Item as='button' onClick={() => {setCurrentModel("");}}>
                                Select a model
                        </Dropdown.Item> 
                    {versions.map((model) => {
                        return (
                            <Dropdown.Item style={{ backgroundColor: model !== productionModel ? '' : 'green' }}
                            key={"#/" + model} as='button' onClick={() => {setCurrentModel(model);}}>
                                    {"Version " + model}
                            </Dropdown.Item>        
                        )
                    })}
                </Dropdown.Menu>
            </Dropdown>
            
            <strong>{(currentModel != '') ? (
                <div>
                    {
                        !loading ? (
                        <div>                  
                            <div style={{display: 'flex', justifyContent: 'space-around', textAlign: 'center', alignItems: 'baseline', fontSize: '18px', width: '100%', height: '100%'}}>  
                                <p>{`${modelName} #${currentModel}`}</p>
                                
                                <Button className={styles.selectVersionButton} variant={currentModel !== productionModel ? 'warning' : 'success'} onClick={setPredictionModel}>{currentModel !== productionModel ? 'Use in Production' : 'Currently Selected'}</Button> 
                            </div>
                            <div className={styles.metrics}>
                                <div>
                                    Accuracy: {modelInfo.history.accuracy}
                                </div>
                                <div>
                                    Loss: {modelInfo.history.loss}
                                </div>
                            </div>
                            <table>
                                <tr>
                                    <th className={styles.header}>Layer</th>
                                    <th className={styles.header}>Datatype</th>
                                    <th className={styles.header}>Units</th>
                                </tr>
                                {((modelInfo.summary != '')) ? getModelSummary().map((obj) => (
                                <tr key={"#" + obj} className={styles.layer}>
                                    <td>{JSON.parse(obj).type}</td>
                                    <td>{JSON.parse(obj).dtype}</td>
                                    <td>{JSON.parse(obj).units}</td>
                                </tr>
                                )) : ""}
                            </table>
                            <div><img src={"data:image/png;base64," + modelInfo.heatmap} alt="Heatmap" /></div>
                        </div>) : (<p>Loading...</p>)
                    }
                </div>
            ) : (<p>Choose version of ({modelName}), in order to see analytics as well as <span style={{color: 'red'}}>re-train.</span></p>)}</strong>
            <FileUploadBox chosenModelVersion={currentModel} updateVersions={updateVersions} modelName={modelName}/>
        </div>
    )
}