const unsafeCopy = (textToCopy: string) => {
  let textArea = document.createElement("textarea");
  textArea.value = textToCopy;
  textArea.style.position = "fixed";
  textArea.style.left = "-999999px";
  textArea.style.top = "-999999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  return new Promise<void>((res, rej) => {
    document.execCommand("copy") ? res() : rej();
    textArea.remove();
  });
};
export const copyToClipboard = (
  textToCopy: string,
  tooltip: {
    snackbar: any;
    transitionComponent?: React.JSXElementConstructor<{
      children: React.ReactElement<any, any>;
    }>;
  }
) => {
  const { snackbar, transitionComponent } = tooltip;
  if (window.isSecureContext && navigator.clipboard)
    navigator.clipboard
      .writeText(textToCopy)
      .then(() => {
        if (snackbar)
          snackbar("copied!", {
            variant: "success",
            TransitionComponent: transitionComponent ?? undefined,
          });
      })
      .catch((error) => {
        console.log("error when copying");
        console.error(error);
        snackbar("not copied!", {
          variant: "error",
          TransitionComponent: transitionComponent ?? undefined,
        });
      });
  else {
    unsafeCopy(textToCopy);
    snackbar("copied!", {
      variant: "success",
      TransitionComponent: transitionComponent,
    });
  }
};
