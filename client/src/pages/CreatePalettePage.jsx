import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import styled from 'styled-components';
import Palette from '../components/Palette';
import FileSelector from '../components/FileSelector';
import api from '../services/api';
import { StyledButton as Button } from '../styles/StyledComponents';

const Container = styled.div`
  display: flex;
  height: 100%;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const ButtonContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
`;

const StyledButton = styled(Button)`
  margin: 10px 10px 0px 10px;
`;

const Image = styled.img`
  max-height: 400px
  max-width: 300px;
  width: 100%;
  height: auto;
  margin: 20px;
`;

const CreatePalettePage = ({ isAuthenticated: checkAuth, authData }) => {
  const history = useHistory();
  const [colours, setColours] = useState([]);
  const [imageFile, setImageFile] = useState();
  const [imageSource, setImageSource] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(checkAuth(authData));
  }, [authData, checkAuth])

  const setImageSourceFromFile = (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImageSource(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const uploadFile = (file) => {
    api.generatePalette(file)
      .then((res) => {
        setImageFile(file);
        setColours(res.colours);
        setImageSourceFromFile(file);
      })
      .catch((err) => { console.log(err); });
  };

  const resetState = () => {
    setColours([]);
    setImageFile();
    setImageSource('');
  };

  const savePalette = async () => {
    if (isAuthenticated) {
      const result = await api.savePalette(imageFile, colours, authData.authToken);
      history.push(`/palettes/${result.id}`);
    }
  };

  const isPaletteGenerated = colours.length > 0 && imageSource;

  return (
    <Container>
      {isPaletteGenerated
        ? (
          <>
            <Palette colours={colours} imageSource={imageSource} />
              <ButtonContainer>
                {isAuthenticated && <StyledButton onClick={savePalette}>Save</StyledButton>}
                <StyledButton onClick={resetState}>Back</StyledButton>
              </ButtonContainer>
          </>
        ) : (
          <>
            <h1>Create a colour palette</h1>
            <FileSelector uploadFile={uploadFile} />
            <Image src='/undraw_add_color_19gv.svg' />
          </>
        )}
    </Container>
  );
};

export default CreatePalettePage;
