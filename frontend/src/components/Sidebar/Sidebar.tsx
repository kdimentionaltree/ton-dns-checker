import React from "react";
import { LightModeOutlined, DarkModeOutlined } from "@mui/icons-material";
import { theme as appTheme } from "../../tools";
import { styled, Typography, useTheme, IconButton, Grid } from "@mui/material";
import { ReactComponent as ReactLogo } from "./icon.svg";

export const Sidebar: React.FC = () => {
  const theme = useTheme();
  const { toggleThemeMode } = React.useContext(appTheme.ThemeModeContext);
  return (
    <Grid container>
      <Grid item xs>
        <Typography
          variant="h5"
          component="div"
          sx={{ flexGrow: 1 }}
          fontWeight="bold"
        >
          <StyledIcon fill={theme.palette.primary.main} />
          TON DNS Checker
        </Typography>
      </Grid>

      <Grid item xs={1} alignContent="end" textAlign="end">
        <IconButton onClick={toggleThemeMode} size="small">
          {theme.palette.mode === appTheme.LIGHT_MODE_THEME ? (
            <DarkModeOutlined color="primary" />
          ) : (
            <LightModeOutlined color="primary" />
          )}
        </IconButton>
      </Grid>
    </Grid>
  );
};
const StyledIcon = styled(ReactLogo)`
  transition: 0.5s;
  vertical-align: middle;
  height: 100%;
  margin-right: 10px;
  &:hover {
    transform: rotateZ(180deg);
  }
`;
