# Estructura de carpetas

Battleship/

│

├── game/

│   ├── ship.py

│   ├── fleet.py

│   ├── board.py

│   ├── placements.py

│   ├── configurations.py

│   ├── game_engine.py

│   ├── runner.py

│   └── fleet_generator.py

│

├── agents/

│   ├── base_agent.py

│   ├── random_agent.py

│   ├── inference.py

│   ├── maximum_probability_agent.py

│   └── maximum_information_gain_agent.py

│

├── experiments/

│   ├── simulation.py

│   ├── evaluation.py

│   ├── benchmark.py

│   └── profile_inference.py

│

├── tests/

│   ├── ...

│

└── main.py


# Módulos y descripciones
- ship.py:	Representación de un barco, sus posiciones y estado de destrucción.
- fleet.py:	Administración de la flota y sus barcos.
- board.py:	Representación del tablero y registro de disparos.
- placements.py:	Generación de todas las ubicaciones posibles para un barco.
- configurations.py:	Generación de configuraciones completas y legales de una flota.
- game_engine.py:	Administración de las reglas y ejecución de los disparos.
- runner.py:	Ejecución de una partida entre un agente y una flota oculta.
- fleet_generator.py:	Generación de flotas para los experimentos.

# Agentes

## RandomAgent

Selecciona aleatoriamente una casilla que todavía no ha sido disparada.

No necesita conocer la flota ni realizar inferencia.


## MaximumProbabilityAgent

Mantiene el conjunto de configuraciones compatibles con las observaciones y calcula la probabilidad marginal de que cada casilla esté ocupada.

Selecciona la casilla con mayor probabilidad de contener un segmento de barco.

## MaximumInformationGainAgent

Evalúa la información esperada que proporcionaría disparar en cada casilla.

Selecciona aquella que maximiza la información mutua entre la configuración oculta y el resultado del disparo.


---

En inference.py tenemos las funciones compartidas:

- is_compatible()
- filter_compatible_configurations()
- calculate_probability_matrix()
- calculate_information_gain()
- print_probability_matrix()

Un aspecto teórico interesante es que nuestros agentes probabilísticos utilizan un posterior uniforme sobre las configuraciones que siguen siendo compatibles con las observaciones.

Por tanto, no estamos entrenando modelos de aprendizaje automático: estamos realizando inferencia exacta sobre un espacio finito de configuraciones.

# Simulación experimentatl (experiments/simulation.py)

Aquí se pueden ejecutar cientos o miles de partidas automáticamente. La función central es:


run_experiment(
    n,
    fleet_lengths,
    agent_classes,
    num_games,
    seed=None
)

Algunas propiedades de esta función son las siguientes:

1. Cada partida utiliza una configuración oculta.
2. Todos los agentes enfrentan la misma configuración en esa partida.
3. Cada agente tiene su propio generaor aleatorio.
4. Las semillas se derivan de manera determinista.
5. El orden de los agentes no altera sus resultados.
6. Podemos repetir experimentos con una semilla conocida.









