import * as React from "react"
import * as ReactDom from "react-dom"

ReactDom.render(<HelloWorld />, document.getElementById("doogle"))

function HelloWorld(){
    return(
        <p>Hello Doogle World</p>
    )
}