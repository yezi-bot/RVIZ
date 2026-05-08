import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_name = 'yezibot_description'
    urdf_name = 'yezibot_base.urdf'

    # 1. 获取功能包路径
    try:
        pkg_path = get_package_share_directory(package_name)
    except Exception as e:
        print(f"错误：找不到功能包 '{package_name}'，请检查是否 source 了环境。")
        return LaunchDescription()

    # 2. 拼接完整路径
    urdf_file_path = os.path.join(pkg_path, 'urdf', urdf_name)
    print(f"正在尝试读取 URDF 文件: {urdf_file_path}")

    # 3. 检查文件是否存在
    if not os.path.exists(urdf_file_path):
        print(f"错误：文件不存在！请检查路径是否正确。")
        return LaunchDescription()

    # 4. 读取文件内容
    with open(urdf_file_path, 'r') as f:
        robot_desc = f.read()

    # 检查内容是否为空
    if len(robot_desc) == 0:
        print(f"错误：文件是空的！请在 {urdf_file_path} 中写入 URDF 内容。")
        return LaunchDescription()

    print("URDF 文件读取成功，长度: " + str(len(robot_desc)) + " 字符")

    # 5. 定义节点
    robot_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen'
        # 注意：这里不要传 arguments，否则它会去等待 robot_description
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_path, 'rviz', 'display.rviz')] # 如果你有保存的rviz配置
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz2_node
    ])