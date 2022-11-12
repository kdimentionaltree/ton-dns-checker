import { Grid, styled, Typography, useMediaQuery } from "@mui/material";
import React from "react";
import { types } from "../../tools";
import { AdvancedGridItem } from "./AdvancedGridItem";

export const DataGridItem: React.FC<types.DataGridItemProps> = ({
  data,
  needMeta,
  isOnline,
  ...restProps
}) => {
  const isDesktop = useMediaQuery("(min-width:900px)");
  return (
    <StyledItem container {...restProps}>
      {needMeta && isDesktop && (
        <Grid item xs={12} md={12}>
          <Grid container position={"relative"}>
            {data.map(
              (el: any, index: number) =>
                !el.disablemeta && (
                  <Grid
                    item
                    xs={el.xs}
                    md={el.md ?? undefined}
                    textAlign="center"
                    key={index}
                  >
                    <Typography variant="h6" fontWeight="bold">
                      {el.label}
                    </Typography>
                  </Grid>
                )
            )}
          </Grid>
        </Grid>
      )}
      <Grid item xs={12} md={12}>
        <Grid container position={"relative"}>
          {data.map((el: any, index: number) => (
            <AdvancedGridItem
              sx={{ opacity: isOnline ? 1 : 0.5 }}
              {...el}
              key={index}
              label={!isDesktop ? el.label : undefined}
            />
          ))}
        </Grid>
      </Grid>
    </StyledItem>
  );
};

const StyledContainer = styled(Grid)`
  margin: 20px auto 0;
  padding: 5px;
`;
const StyledItem = styled(StyledContainer)`
  margin-top: 5px;
  box-sizing: border-box;
  padding-bottom: 10px;
  text-align: start;
`;
