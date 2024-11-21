import sim
import numpy as np
import time

def connect_to_simulator():
    # Conectar-se ao CoppeliaSim
    sim.simxFinish(-1)  # Garantir que qualquer conexão anterior seja fechada
    clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Conectar via Remote API
    if clientID == -1:
        print("Não foi possível conectar ao CoppeliaSim!")
        exit()
    return clientID

def get_robot_handles(clientID):
    # Obter os manipuladores do robô e sensores
    errorCode, robotHandle = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx', sim.simx_opmode_blocking)
    errorCode, laserHandle = sim.simxGetObjectHandle(clientID, 'Pioneer_p3dx_laser', sim.simx_opmode_blocking)
    return robotHandle, laserHandle

def send_velocity_commands(clientID, linear_velocity, angular_velocity):
    # Enviar comandos de velocidade ao CoppeliaSim
    sim.simxSetFloatSignal(clientID, 'linearVelocity', linear_velocity, sim.simx_opmode_oneshot)
    sim.simxSetFloatSignal(clientID, 'angularVelocity', angular_velocity, sim.simx_opmode_oneshot)

def get_laser_data(clientID):
    # Coletar dados do sensor laser
    errorCode, laserData = sim.simxGetStringSignal(clientID, 'laserData', sim.simx_opmode_blocking)
    laserData = laserData.decode('utf-8')  # Decodificar os dados como string
    distances = np.array([float(d) for d in laserData.split(',')])  # Converter os dados em lista de floats
    return distances

def main():
    clientID = connect_to_simulator()
    robotHandle, laserHandle = get_robot_handles(clientID)

    # Inicializar SLAM ou outras lógicas necessárias (não mostrado aqui)
    linear_velocity = 1.0  # Velocidade linear (m/s)
    angular_velocity = 0.0  # Velocidade angular (rad/s)
    
    try:
        while True:
            # Enviar comandos de movimento ao robô
            send_velocity_commands(clientID, linear_velocity, angular_velocity)

            # Obter dados do laser
            laser_data = get_laser_data(clientID)
            print("Dados do Laser:", laser_data)

            # Aqui você pode aplicar seu algoritmo SLAM usando os dados do laser (exemplo simples)
            # Usar os dados do laser para mapear o ambiente ou processar o SLAM

            # Atraso para simulação de tempo real
            time.sleep(0.1)
            
            # Exemplo: se um obstáculo for detectado, gira o robô
            if np.min(laser_data) < 1.0:  # Se algum obstáculo estiver a menos de 1 metro
                angular_velocity = 0.5  # Gira o robô
            else:
                angular_velocity = 0.0  # Movimenta em linha reta

    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    
    finally:
        # Parar o robô ao final
        send_velocity_commands(clientID, 0, 0)
        sim.simxFinish(clientID)  # Fechar a conexão

if __name__ == "__main__":
    main()
