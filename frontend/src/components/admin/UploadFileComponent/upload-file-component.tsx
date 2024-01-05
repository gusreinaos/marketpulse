//Author: Aditya Kadkhikar, Burak Askan
import {useState, useEffect} from 'react'
import styles from './upload-file-component.module.scss'
import ModelService from '../../../services/modelService';
import Button from 'react-bootstrap/Button';
import tick from '../../../assets/tick.svg';
import cross from '../../../assets/cross.svg';

export interface IModelTrainProp {
    modelName: string;
    chosenModelVersion: string;
    updateVersions: (newValue: string) => void;
}

export const FileUploadBox = (props: IModelTrainProp) => {
    const [file, setFile] = useState("");
    const [uploaded, setUploaded] = useState(false);
    const [variant, setVariant] = useState('primary');
    const [training, setTraining] = useState('Train Model')


    const onInputChange = (e: any) => {
        setFile(e.target.files[0]);
        console.log(e.target.files[0]);
    };

    useEffect(() => {
        if (file == "" || file == undefined) {
            setUploaded(false);
        } else {
            setUploaded(true);
        }
    }, [file])

    const onUpload = async (e: any) =>  {
        setTraining('Training Model')
        setVariant('warning')

        const data = new FormData();
        data.append('csv-to-train', file);
        let returned_value : string = ""
        if(props.modelName === "Market Trend Model") {
            returned_value = await ModelService.trainMarketTrendModel(props.chosenModelVersion, data);
        }else if("Sentiment Model"){
            returned_value = await ModelService.trainSentimentModel(props.chosenModelVersion, data);
        }

        console.log(returned_value)

        if(returned_value !== "" && returned_value !== undefined && returned_value && returned_value !== 'false') {
            props.updateVersions(returned_value)
            setVariant('success')
            setTraining('Trained!')
            const timeoutId = setTimeout(() => {
                setVariant('primary')
                setTraining('Train Model')
              }, 4000);
        }else {
            setVariant('danger')
            setTraining('Training Failed')
        }
        
    }

    return (
        (props.chosenModelVersion != '') ? 
            (<form className={styles.fileUpload}>
                <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                    <label>Upload a valid CSV here.</label>
                    <div style={{display: 'flex', alignContent:'baseline'}}>
                        <input type="file" required={true} 
                        className='csv-upload' onChange={onInputChange} 
                        accept='text/csv, .csv'/>
                        {   
                            
                                <div>
                                    <Button style={{fontSize:'18px', display:'flex', alignContent:'baseline'}} variant={variant} onClick={onUpload}>
                                        {training}  
                                        {training == 'Training Model' ? <div className={styles.loader}> </div>
                                            :
                                            <div>
                                                {training == 'Trained!' ? <img src={tick} alt='Tick' className={styles.tick}/> :
                                                <div>
                                                    {training == 'Training Failed' ? <img src={cross} alt='Cross' className={styles.cross}/>:<div></div>}
                                            
                                                </div>}
                                            </div>
                                        }
                                        
                                    </Button> 
                                    
                                </div>
                                
                        }
                    </div>
                </div>
            </form>) : 
        (<div></div>)
    )
}