import {
  Button,
  Grid,
  Popover,
  styled,
  ToggleButton,
  ToggleButtonGroup,
  Typography,
} from "@mui/material";
import React from "react";
import { DHTDataGrid, LSDataGrid } from "./";
import { types } from "../../tools";

const compareResolved = (
  data: types.DHTResolvedType[] | types.LSResolvedType[]
) => {
  let map = new Map();
  data.forEach((e) => {
    const key =
      "adnl" in e ? e.adnl : e.ip && e.port ? `${e.ip}:${e.port}` : null;
    map.has(key) ? map.get(key).count++ : map.set(key, { count: 1 });
  });
  return map;
};
export const DataGrid: React.FC<types.DataGridProps> = ({
  dhtData,
  lsData,
  selectedTable,
  setSelectedTable,
  disabled,
}) => {
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(
    null
  );
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "resolved-popper" : undefined;
  const hasResolved = !!dhtData.resolved.length || !!lsData.resolved.length;
  return (
    <Grid container columnSpacing="20px">
      <Grid item xs={12} lg={12}>
        <Grid container>
          <Grid item xs={0} md={hasResolved ? 2 : 0}></Grid>
          <Grid item xs={hasResolved ? 10 : 12} md={hasResolved ? 8 : 12}>
            <ToggleButtonGroup
              color="secondary"
              value={selectedTable}
              exclusive
              onChange={(event: React.MouseEvent<HTMLElement>, value: string) =>
                setSelectedTable(value as "DHT" | "LS")
              }
            >
              <ToggleButton
                value="LS"
                disabled={disabled && selectedTable === "DHT"}
              >
                <Typography variant="h6" fontWeight="bold">
                  LS
                </Typography>
              </ToggleButton>
              <ToggleButton
                value="DHT"
                disabled={disabled && selectedTable === "LS"}
              >
                <Typography variant="h6" fontWeight="bold">
                  DHT
                </Typography>
              </ToggleButton>
            </ToggleButtonGroup>
          </Grid>
          {hasResolved && (
            <Grid
              item
              xs={2}
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "end",
              }}
            >
              <Button
                size="small"
                color="secondary"
                onClick={handleClick}
                aria-describedby={id}
              >
                Compare Resolved
              </Button>
              <Popover
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                  vertical: "bottom",
                  horizontal: "right",
                }}
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
              >
                <PopperContainer style={{ padding: "10px" }}>
                  {Array.from(
                    compareResolved(
                      selectedTable === "DHT"
                        ? dhtData.resolved
                        : lsData.resolved
                    ),
                    ([name, value]) => ({ name, value })
                  ).map(({ name, value }) => (
                    <PopperItem key={name + value} style={{ margin: "5px" }}>
                      {name ?? "not resolved"} - count: {value.count}
                    </PopperItem>
                  ))}
                </PopperContainer>
              </Popover>
            </Grid>
          )}
        </Grid>

        {selectedTable === "DHT" ? (
          <DHTDataGrid {...dhtData} />
        ) : (
          <LSDataGrid {...lsData} />
        )}
      </Grid>
    </Grid>
  );
};
const PopperContainer = styled("div")`
  padding: "10px";
`;
const PopperItem = styled("p")`
  margin: "5px";
  overflow: hidden;
  text-overflow: ellipsis;
`;
