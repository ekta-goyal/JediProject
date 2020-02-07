function Navigation() {
    return ( <h5>Navigation</h5>);
}
function Side() {
    return (<h1>Side bar</h1>)
}
function Main() {
    return (<h1>Main</h1>)
}
function Footer() {
    return (<h1>Footer</h1>)
}
function App() {
    return (
        <div>
            <Navigation />
            <div className="main">
                <Side />
                <Main />
            </div>
            <Footer />
        </div>
    );
  }

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);