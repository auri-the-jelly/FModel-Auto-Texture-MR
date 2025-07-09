import bpy

def create_normal_converter():
    # Check if the node group already exists
    if 'Normal_Convert' in bpy.data.node_groups:
        return  # If it exists, no need to recreate it

    # create a group
    normal_convert_group = bpy.data.node_groups.new('Normal_Convert', 'ShaderNodeTree')
    print("create_normal_converter executing...")
    # create group inputs
    group_inputs = normal_convert_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-500, 0)
    normal_convert_group.interface.new_socket("Color", in_out='INPUT', socket_type='NodeSocketColor', parent=None)
    normal_convert_group.interface.new_socket("Factor", in_out='INPUT', socket_type='NodeSocketFloat', parent=None)

    # create group output
    group_outputs = normal_convert_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (500, 0)
    normal_convert_group.interface.new_socket("Color", in_out='OUTPUT', socket_type='NodeSocketColor', parent=None)

    # create nodes
    node_separate_rgb = normal_convert_group.nodes.new('ShaderNodeSeparateRGB')
    node_separate_rgb.location = (-300, 0)

    node_invert = normal_convert_group.nodes.new('ShaderNodeInvert')
    node_invert.location = (0, 100)

    node_mix = normal_convert_group.nodes.new('ShaderNodeMixRGB')
    node_mix.location = (100, 0)

    node_combine_rgb = normal_convert_group.nodes.new('ShaderNodeCombineRGB')
    node_combine_rgb.location = (300, 0)

    # link nodes together
    normal_convert_group.links.new(node_separate_rgb.outputs['R'], node_combine_rgb.inputs['R'])
    normal_convert_group.links.new(node_separate_rgb.outputs['B'], node_combine_rgb.inputs['B'])

    normal_convert_group.links.new(node_separate_rgb.outputs['G'], node_invert.inputs['Color'])
    normal_convert_group.links.new(node_invert.outputs['Color'], node_mix.inputs[2])

    normal_convert_group.links.new(node_separate_rgb.outputs['G'], node_mix.inputs[1])
    normal_convert_group.links.new(group_inputs.outputs['Factor'], node_mix.inputs[0])

    normal_convert_group.links.new(node_mix.outputs['Color'], node_combine_rgb.inputs['G'])

    # link inputs and outputs to the group
    normal_convert_group.links.new(group_inputs.outputs['Color'], node_separate_rgb.inputs['Image'])
    normal_convert_group.links.new(node_combine_rgb.outputs['Image'], group_outputs.inputs['Color'])
