import React from "react";
import { createTheme, responsiveFontSizes } from "@mui/material";

export interface IThemeModeContext {
  toggleThemeMode: () => void;
}

export const ThemeModeContext = React.createContext<IThemeModeContext>(
  {} as IThemeModeContext
);
export const DARK_MODE_THEME = "dark";
export const LIGHT_MODE_THEME = "light";
const colors = {
  white: "#fff",
  blue_dark: "#2596be",
  blue_light: "#2596be",
  dark: "#232328",
};
export const getAppTheme = (
  mode: typeof LIGHT_MODE_THEME | typeof DARK_MODE_THEME
) => {
  let theme = createTheme({
    palette: {
      mode: mode,
      warning: {
        main: "#FF2400",
      },
      success: {
        main: "#004524",
      },
      ...(mode === "dark"
        ? {
            primary: {
              main: colors.white,
            },
            secondary: {
              main: colors.blue_light,
            },
          }
        : {
            primary: {
              main: colors.dark,
            },
            secondary: {
              main: colors.blue_dark,
            },
          }),
    },
    typography: {
      fontFamily: ["Mulish", "sans-serif"].join(","),
      fontSize: 12,
    },
  });
  theme = responsiveFontSizes(theme);

  return theme;
};
