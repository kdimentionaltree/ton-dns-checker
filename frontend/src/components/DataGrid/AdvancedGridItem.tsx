import { Grid, styled, Fade, IconButton } from "@mui/material";
import React from "react";
import { useSnackbar } from "notistack";
import { ContentCopyOutlined } from "@mui/icons-material";
import { copy, types } from "../../tools";

export const AdvancedGridItem: React.FC<types.AdvancedGridItemProps> = ({
  label,
  content,
  isLink,
  ...restProps
}) => {
  const ref = React.createRef<HTMLSpanElement>();
  const { enqueueSnackbar } = useSnackbar();
  const handleClick = () => {
    copy.copyToClipboard(ref.current?.innerText ?? "", {
      snackbar: enqueueSnackbar,
      transitionComponent: Fade,
    });
  };

  return (
    <Grid item {...restProps}>
      {label && <Label>{label}</Label>}
      {isLink ? (
        <StyledDiv>
          <span ref={ref}>{content}</span>
          <StyledIcon onClick={handleClick} size="small" color="secondary">
            <ContentCopyOutlined fontSize="small" />
          </StyledIcon>
        </StyledDiv>
      ) : (
        content
      )}
    </Grid>
  );
};

const Label = styled("p")`
  margin: 0;
  font-weight: bold;
  font-size: 0.9em;
`;
const StyledDiv = styled("div")`
  display: flex;
  justify-content: center;
  span {
    max-width: 95%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
`;
const StyledIcon = styled(IconButton)`
  padding: 0px 5px;
`;
