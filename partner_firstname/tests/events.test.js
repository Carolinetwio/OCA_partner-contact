test("press 'Enter' on form input", async () => {
    await mountOnFixture(/* xml */ `
        <form t-on-submit.prevent="">
            <input type="text" />
        </form>
    `);
    monitorEvents("form");
    monitorEvents("input");

    expect("input").not.toBeFocused();

    await press("Tab");
    await animationFrame();

    expect("input").toBeFocused();

    await press("Enter");
    await animationFrame();

    expect.verifySteps([
        // Tab
        "focus@input",
        "focusin@input",
        "focusin@form",
        "pointerover@input",
        "pointerover@form",
        "pointerenter@form",
        "pointerenter@input",
        "mouseover:0@input",
        "mouseover:0@form",
        "mouseenter:0@form",
        "mouseenter:0@input",
        "select@input",
        "select@form",
        // Enter
        "keydown:Enter@input",
        "keydown:Enter@form",
        "submit@form",
        "keyup:Enter@input",
        "keyup:Enter@form",
    ]);
});
