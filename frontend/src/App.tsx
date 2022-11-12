import React from "react";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { theme as appTheme } from "./tools";
import { QueryClient, QueryClientProvider } from "react-query";
import { styled } from "@mui/material";
import { Sidebar } from "./components/Sidebar";
import Main from "./components/Main";
import { SnackbarProvider } from "notistack";

const queryClient = new QueryClient();
const App: React.FC = () => {
  const systemThemeMode =
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
      ? appTheme.DARK_MODE_THEME
      : appTheme.LIGHT_MODE_THEME;
  const [mode, setMode] = React.useState<
    typeof appTheme.LIGHT_MODE_THEME | typeof appTheme.DARK_MODE_THEME
  >((localStorage.getItem("theme") as "light" | "dark") ?? systemThemeMode);
  const themeMode = React.useMemo(
    () => ({
      toggleThemeMode: () => {
        let newTheme: "light" | "dark";
        setMode((prevMode) => {
          newTheme =
            prevMode === appTheme.LIGHT_MODE_THEME
              ? appTheme.DARK_MODE_THEME
              : appTheme.LIGHT_MODE_THEME;
          return newTheme;
        });
        setTimeout(() => localStorage.setItem("theme", newTheme));
      },
    }),
    []
  );

  const theme = React.useMemo(() => appTheme.getAppTheme(mode), [mode]);

  return (
    <appTheme.ThemeModeContext.Provider value={themeMode}>
      <SnackbarProvider maxSnack={1} preventDuplicate autoHideDuration={1500}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Wrapper>
            <Sidebar />
            <ContentWrapper>
              <QueryClientProvider client={queryClient}>
                <Main />
              </QueryClientProvider>
            </ContentWrapper>
          </Wrapper>
        </ThemeProvider>
      </SnackbarProvider>
    </appTheme.ThemeModeContext.Provider>
  );
};
const Wrapper = styled("div")`
  margin: 20px auto;
  max-width: 1180px;
`;
const ContentWrapper = styled("div")`
  margin: 20px 0;
`;
export default App;
