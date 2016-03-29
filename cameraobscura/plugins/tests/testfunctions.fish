function twrvrplugin
    cd ../
    tangleweave rvrplugin.pnw
    cd tests/steps/
end

function rvrpluginfeature
    twrvrplugin
    tangleweave rvrpluginfeature.pnw
    cd ../
    behave features/rvrplugin.feature
end

function dutconfigurationfeature
    twrvrplugin
    tangleweave dutconfigurationfeature.pnw
    cd ../
    behave features/dutconfiguration.feature
end

function attenuationconfigurationfeature
    twrvrplugin
    tangleweave attenuationconfigurationfeature.pnw
    cd ../
    behave features/attenuationconfiguration.feature
end

function otherconfigurationfeature
    twrvrplugin
    tangleweave otherconfigurationfeature.pnw
    cd ../
    behave features/otherconfiguration.feature
end

function iperfconfigurationfeature
    twrvrplugin
    tangleweave iperfconfigurationfeature.pnw
    cd ../
    behave features/iperfconfiguration.feature
end

function queryconfigurationfeature
    twrvrplugin
    tangleweave queryconfigurationfeature.pnw
    cd ../
    behave features/queryconfiguration.feature
end

function testall
    twrvrplugin
    tangleweave *.pnw
    cd ../
    behave
end
