import { Button, Grid, TextField, styled } from "@mui/material";
import React from "react";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import { types } from "../tools";
const Search: React.FC<types.SearchProps> = ({ onSearch, value }) => {
  const [state, setState] = React.useState(value);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState(event.target.value);
  };

  const onSubmit = () => {
    onSearch(state.trim());
  };

  const onKeyUp = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === "Enter") {
      e.preventDefault();
      onSearch(state.trim());
    }
  };

  return (
    <StyledContainer
      container
      textAlign="center"
      alignItems="center"
      justifyContent="center"
    >
      <Grid item xs={12} md={6}>
        <TextField
          variant="outlined"
          value={state}
          onChange={handleChange}
          label="Domain or ADNL address in hex form"
          color="secondary"
          size="small"
          onBlur={onSubmit}
          onKeyUp={onKeyUp}
          fullWidth
        />
      </Grid>
      <Grid item xs={12} md={1} alignContent="end" textAlign="end">
        <StyledButton
          startIcon={<SearchOutlinedIcon />}
          disabled={!state}
          onClick={onSubmit}
        >
          check
        </StyledButton>
      </Grid>
    </StyledContainer>
  );
};
const StyledContainer = styled(Grid)`
  text-align: center;
  margin-bottom: 20px;
`;
const StyledButton = styled(Button)`
  margin: auto 0;
  height: 100%;
`;
export default Search;
