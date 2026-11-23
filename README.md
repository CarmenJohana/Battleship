

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


Módulos y descripciones
- ship.py:	Representación de un barco, sus posiciones y estado de destrucción.
- fleet.py:	Administración de la flota y sus barcos.
- board.py:	Representación del tablero y registro de disparos.
- placements.py:	Generación de todas las ubicaciones posibles para un barco.
- configurations.py:	Generación de configuraciones completas y legales de una flota.
- game_engine.py:	Administración de las reglas y ejecución de los disparos.
- runner.py:	Ejecución de una partida entre un agente y una flota oculta.
- fleet_generator.py:	Generación de flotas para los experimentos.



