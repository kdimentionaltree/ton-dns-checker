import { Grid, useTheme, CircularProgress, Typography } from "@mui/material";
import React from "react";
import { types } from "../../../tools";
import { DataGridItem } from "../DataGridItem";
import { Done, Close } from "@mui/icons-material";

const getResolved = (adnl: string | null) => (adnl ? `${adnl}` : "-");

export const LSDataGrid: React.FC<types.LSDataGridProps> = ({
  data,
  resolved,
  isLoading,
}) => {
  const theme = useTheme();
  const gridSx = {
    "&:not(:last-of-type)": {
      borderBottom: `1px solid ${theme.palette.primary.main}`,
    },
  };
  const hasValues = resolved.some((e) => e && e.adnl !== null);
  return (
    <Grid container>
      {data.map((el, index) => (
        <Grid
          item
          xs={12}
          key={el.idx + el.ip}
          sx={{ ...gridSx, opacity: el.is_online ? 1 : 0.7 }}
        >
          <DataGridItem
            key={el.key}
            isOnline={el.is_online}
            data={[
              {
                xs: 2,
                md: true,
                label: "Idx",
                content: (
                  <div style={{ display: "flex", justifyContent: "center" }}>
                    {el.is_online ? (
                      <Done
                        style={{ fill: "green" }}
                        fontSize="medium"
                        sx={{ position: "absolute", left: 0 }}
                      />
                    ) : (
                      <Close
                        style={{ fill: "red" }}
                        fontSize="medium"
                        sx={{ position: "absolute", left: 0 }}
                      />
                    )}

                    <Typography
                      variant="body1"
                      sx={{ marginLeft: "3px" }}
                      fontWeight="bold"
                    >
                      {el.idx}
                    </Typography>
                  </div>
                ),
                textAlign: "center",
              },
              {
                xs: 10,
                md: hasValues ? 2 : 3,
                label: "IP:port",
                content: `${el.ip}:${el.port}`,
                isLink: true,
                textAlign: "center",
              },
              {
                xs: 12,
                md: hasValues ? 2 : 5,
                label: "Key",
                content: el.key,
                isLink: true,
                textAlign: "center",
              },
              {
                xs: 12,
                md: hasValues ? 7 : 3,
                order: { xs: 3, md: 4 },
                label: "ADNL",
                textAlign: "center",
                margin: "auto",
                content: isLoading ? (
                  <CircularProgress color="secondary" size="1em" />
                ) : resolved[index] ? (
                  getResolved(resolved[index].adnl)
                ) : (
                  "-"
                ),
                isLink:
                  !!resolved[index] && !!resolved[index].adnl && !isLoading,
              },
            ]}
            needMeta={index === 0}
          />
        </Grid>
      ))}
    </Grid>
  );
};
